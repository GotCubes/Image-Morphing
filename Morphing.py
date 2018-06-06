#! /usr/bin/env python3.4

import os
import imageio
import numpy as np
from PIL import Image, ImageDraw
from scipy import interpolate, spatial

class Affine:
    def __init__(self, source, destination):
        # Validate source input.
        if source.dtype != 'float64':
            raise ValueError("source must be a numpy array of type float64.")
        if source.shape != (3, 2):
            raise ValueError("source must be a 3x2 array.")

        # Validate destination input.
        if destination.dtype != 'float64':
            raise ValueError("destination must be a numpy array of type float64.")
        if destination.shape != (3, 2):
            raise ValueError("destination must be a 3x2 array.")

        # Define combined source data matrix.
        A = np.array([[source[0, 0], source[0, 1], 1, 0, 0, 0],
                      [0, 0, 0, source[0, 0], source[0, 1], 1],
                      [source[1, 0], source[1, 1], 1, 0, 0, 0],
                      [0, 0, 0, source[1, 0], source[1, 1], 1],
                      [source[2, 0], source[2, 1], 1, 0, 0, 0],
                      [0, 0, 0, source[2, 0], source[2, 1], 1]], dtype = 'float64')

        # Define combined destination matrix.
        b = np.reshape(destination, (6, 1))

        # Solve for transformation matrix.
        h = np.linalg.solve(A, b)

        # Define combined transformation matrix data.
        matrix = np.vstack([np.reshape(h, (2, 3)), [0, 0, 1]])

        # Initialize affine transform data.
        self.source = source
        self.destination = destination
        self.matrix = matrix

    def transform(self, sourceImage, destinationImage):
        # Validate sourceImage input.
        if not isinstance(sourceImage, np.ndarray):
            raise TypeError("sourceImage must be a numpy array.")

        # Validate destinationImage input.
        if not isinstance(destinationImage, np.ndarray):
            raise TypeError("destinationImage must be a numpy array.")

        # Define vectorizations.
        hInv = np.linalg.inv(self.matrix)
        getCoord = np.vectorize(lambda x, y, a: hInv[a, 0] * y + hInv[a, 1] * x + hInv[a, 2], otypes = [np.float64])

        # Generate spline.
        xRange = np.arange(np.amin(self.source[:, 1]), np.amax(self.source[:, 1]), 1)
        yRange = np.arange(np.amin(self.source[:, 0]), np.amax(self.source[:, 0]), 1)
        zRange = sourceImage[int(xRange[0]):int(xRange[-1] + 1), int(yRange[0]):int(yRange[-1] + 1)]
        spline = interpolate.RectBivariateSpline(xRange, yRange, zRange, kx = 1, ky = 1)

        # Generate transformation mask.
        mask = Image.new('L', (destinationImage.shape[1], destinationImage.shape[0]), 0)
        ImageDraw.Draw(mask).polygon(self.destination.ravel().tolist(), outline = 255, fill = 255)
        xp, yp = np.nonzero(mask)

        # Find transformed coordinates and values.
        x = getCoord(xp, yp, 1)
        y = getCoord(xp, yp, 0)
        destinationImage[xp, yp] = spline.ev(x, y)

class Blender:
    def __init__(self, startImage, startPoints, endImage, endPoints):
        # Validate startImage input.
        if not isinstance(startImage, np.ndarray):
            raise TypeError("startImage must be a numpy array.")

        # Validate startPoints input.
        if not isinstance(startPoints, np.ndarray):
            raise TypeError("startPoints must be a numpy array.")

        # Validate endImage input.
        if not isinstance(endImage, np.ndarray):
            raise TypeError("endImage must be a numpy array.")

        # Validate endPoints input.
        if not isinstance(endPoints, np.ndarray):
            raise TypeError("endPoints must be a numpy array.")

        # Define triangulation.
        simplices = spatial.Delaunay(startPoints).simplices

        # Initialize blender data.
        self.startImage = startImage
        self.startPoints = startPoints
        self.endImage = endImage
        self.endPoints = endPoints
        self.simplices = simplices

    def getBlendedImage(self, alpha):
        # Initialize blended image components.
        target1 = np.empty(self.startImage.shape, dtype = 'float64')
        target2 = np.empty(self.endImage.shape, dtype = 'float64')

        # Process all triangles.
        targets = (1 - alpha) * self.startPoints + alpha * self.endPoints
        for triangle in self.simplices.tolist():
            # Define relevant points.
            src = self.startPoints[triangle]
            dst = self.endPoints[triangle]
            tar = targets[triangle]

            # Define affine transforms.
            Affine(src, tar).transform(self.startImage, target1)
            Affine(dst, tar).transform(self.endImage, target2)

        # Alpha blend images.
        target = (1 - alpha) * target1 + alpha * target2

        return target.astype('uint8')

    def generateMorphVideo(self, targetFolderPath, sequenceLength, includeReversed):
        # Create target folder path if it does not already exist.
        if not os.path.exists(targetFolderPath): os.makedirs(targetFolderPath)

        # Initialize MP4
        writer = imageio.get_writer(targetFolderPath + '/morph.mp4', fps = 5, macro_block_size = None)
        frames = np.empty([sequenceLength, self.startImage.shape[0], self.startImage.shape[1]], dtype = 'uint8')

        # Save initial frame.
        frame = self.startImage
        frames[0] = frame

        # Save initial image.
        frame = Image.fromarray(frame).convert('L')
        frame.save(targetFolderPath + '/frame001.jpg')

        if includeReversed:
            frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(sequenceLength * 2))

        # Generate blends.
        i = 2
        for alpha in np.arange(1 / (sequenceLength - 1), 1, 1 / (sequenceLength - 1)).tolist():
            # Save frame.
            frame = self.getBlendedImage(alpha)
            frames[i - 1] = frame

            # Save image.
            frame = Image.fromarray(frame).convert('L')
            frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(i))

            if includeReversed:
                frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(sequenceLength * 2 - i + 1))

            i += 1

        # Save final frame.
        frame = self.endImage
        frames[-1] = frame

        # Save final image.
        frame = Image.fromarray(self.endImage).convert('L')
        frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(i))

        if includeReversed:
            frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(sequenceLength + 1))

        # Append forward frames.
        for frame in frames:
            writer.append_data(frame)

        # Append reversed frames.
        if includeReversed:
            for frame in np.flip(frames, 0):
                writer.append_data(frame)

        # Finalize MP4
        writer.close()

class ColorAffine:
    def __init__(self, source, destination):
        # Validate source input.
        if source.dtype != 'float64':
            raise ValueError("source must be a numpy array of type float64.")
        if source.shape != (3, 2):
            raise ValueError("source must be a 3x2 array.")

        # Validate destination input.
        if destination.dtype != 'float64':
            raise ValueError("destination must be a numpy array of type float64.")
        if destination.shape != (3, 2):
            raise ValueError("destination must be a 3x2 array.")

        # Define combined source data matrix.
        A = np.array([[source[0, 0], source[0, 1], 1, 0, 0, 0],
                      [0, 0, 0, source[0, 0], source[0, 1], 1],
                      [source[1, 0], source[1, 1], 1, 0, 0, 0],
                      [0, 0, 0, source[1, 0], source[1, 1], 1],
                      [source[2, 0], source[2, 1], 1, 0, 0, 0],
                      [0, 0, 0, source[2, 0], source[2, 1], 1]], dtype = 'float64')

        # Define combined destination matrix.
        b = np.reshape(destination, (6, 1))

        # Solve for transformation matrix.
        h = np.linalg.solve(A, b)

        # Define combined transformation matrix data.
        matrix = np.vstack([np.reshape(h, (2, 3)), [0, 0, 1]])

        # Initialize affine transform data.
        self.source = source
        self.destination = destination
        self.matrix = matrix

    def transform(self, sourceImage, destinationImage):
        # Validate sourceImage input.
        if not isinstance(sourceImage, np.ndarray):
            raise TypeError("sourceImage must be a numpy array.")

        # Validate destinationImage input.
        if not isinstance(destinationImage, np.ndarray):
            raise TypeError("destinationImage must be a numpy array.")

        # Define vectorizations.
        hInv = np.linalg.inv(self.matrix)
        getCoord = np.vectorize(lambda x, y, a: hInv[a, 0] * y + hInv[a, 1] * x + hInv[a, 2], otypes = [np.float64])

        # Generate spline.
        xRange = np.arange(np.amin(self.source[:, 1]), np.amax(self.source[:, 1]), 1)
        yRange = np.arange(np.amin(self.source[:, 0]), np.amax(self.source[:, 0]), 1)
        zRange = sourceImage[int(xRange[0]):int(xRange[-1] + 1), int(yRange[0]):int(yRange[-1] + 1)]
        rSpline = interpolate.RectBivariateSpline(xRange, yRange, np.compress([1, 0, 0], zRange, axis = 2), kx = 1, ky = 1)
        gSpline = interpolate.RectBivariateSpline(xRange, yRange, np.compress([0, 1, 0], zRange, axis = 2), kx = 1, ky = 1)
        bSpline = interpolate.RectBivariateSpline(xRange, yRange, np.compress([0, 0, 1], zRange, axis = 2), kx = 1, ky = 1)


        # Generate transformation mask.
        mask = Image.new('L', (destinationImage.shape[1], destinationImage.shape[0]), 0)
        ImageDraw.Draw(mask).polygon(self.destination.ravel().tolist(), outline = 255, fill = 255)
        xp, yp = np.nonzero(mask)

        # Find transformed coordinates and values.
        x = getCoord(xp, yp, 1)
        y = getCoord(xp, yp, 0)
        destinationImage[xp, yp] = np.transpose([rSpline.ev(x, y), gSpline.ev(x, y), bSpline.ev(x, y)])

class ColorBlender:
    def __init__(self, startImage, startPoints, endImage, endPoints):
        # Validate startImage input.
        if not isinstance(startImage, np.ndarray):
            raise TypeError("startImage must be a numpy array.")

        # Validate startPoints input.
        if not isinstance(startPoints, np.ndarray):
            raise TypeError("startPoints must be a numpy array.")

        # Validate endImage input.
        if not isinstance(endImage, np.ndarray):
            raise TypeError("endImage must be a numpy array.")

        # Validate endPoints input.
        if not isinstance(endPoints, np.ndarray):
            raise TypeError("endPoints must be a numpy array.")

        # Define triangulation.
        simplices = spatial.Delaunay(startPoints).simplices

        # Initialize blender data.
        self.startImage = startImage
        self.startPoints = startPoints
        self.endImage = endImage
        self.endPoints = endPoints
        self.simplices = simplices

    def getBlendedImage(self, alpha):
        # Initialize blended image components.
        target1 = np.empty(self.startImage.shape, dtype = 'float64')
        target2 = np.empty(self.endImage.shape, dtype = 'float64')

        # Process all triangles.
        targets = (1 - alpha) * self.startPoints + alpha * self.endPoints
        for triangle in self.simplices.tolist():
            # Define relevant points.
            src = self.startPoints[triangle]
            dst = self.endPoints[triangle]
            tar = targets[triangle]

            # Define affine transforms.
            ColorAffine(src, tar).transform(self.startImage, target1)
            ColorAffine(dst, tar).transform(self.endImage, target2)

        # Alpha blend images.
        target = (1 - alpha) * target1 + alpha * target2

        return target.astype('uint8')

    def generateMorphVideo(self, targetFolderPath, sequenceLength, includeReversed):
        # Create target folder path if it does not already exist.
        if not os.path.exists(targetFolderPath): os.makedirs(targetFolderPath)

        # Initialize MP4
        writer = imageio.get_writer(targetFolderPath + '/morph.mp4', fps = 5, macro_block_size = None)
        frames = np.empty([sequenceLength, self.startImage.shape[0], self.startImage.shape[1], self.startImage.shape[2]], dtype = 'uint8')

        # Save initial frame.
        frame = self.startImage
        frames[0] = frame

        # Save initial image.
        frame = Image.fromarray(frame).convert('RGB')
        frame.save(targetFolderPath + '/frame001.jpg')

        if includeReversed:
            frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(sequenceLength * 2))

        # Generate blends.
        i = 2
        for alpha in np.arange(1 / (sequenceLength - 1), 1, 1 / (sequenceLength - 1)).tolist():
            # Save frame.
            frame = self.getBlendedImage(alpha)
            frames[i - 1] = frame

            # Save image.
            frame = Image.fromarray(frame).convert('RGB')
            frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(i))

            if includeReversed:
                frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(sequenceLength * 2 - i + 1))

            i += 1

        # Save final frame.
        frame = self.endImage
        frames[-1] = frame

        # Save final image.
        frame = Image.fromarray(frame).convert('RGB')
        frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(i))

        if includeReversed:
            frame.save(targetFolderPath + '/frame{:03d}.jpg'.format(sequenceLength + 1))

        # Append forward frames.
        for frame in frames:
            writer.append_data(frame)

        # Append reversed frames.
        if includeReversed:
            for frame in np.flip(frames, 0):
                writer.append_data(frame)

        # Finalize MP4
        writer.close()

if __name__ == "__main__":
    startImage = imageio.imread('WolfColor.jpg')
    startPoints = np.loadtxt('wolf.jpg.txt')
    endImage = imageio.imread('Tiger2Color.jpg')
    endPoints = np.loadtxt('tiger2.jpg.txt')

    blender = ColorBlender(startImage, startPoints, endImage, endPoints)

    frame = blender.getBlendedImage(0.5)
    Image.fromarray(frame).convert('RGB').save('BlendedColor.jpg')

    # blender.generateMorphVideo('testResults/personalResults', 50, True)
