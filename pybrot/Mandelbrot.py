import logging
import numpy as np
from numpy import log, log2
from random import choice
from .ComplexDraw import ComplexDraw as CD
from .MandelColoring import IterativeColor

class Mandelbrot:

    def __init__(self, x=-0.7, y=0, drawRadius=2, autoMaxIter=True,
                 blacknessLimit=0.3, maxIterations=64, escapeRadius=4, samples=250,
                 coloringFunc=None, saturation=0.9):
        # Define what the image will look like
        self.x = x
        self.y = y
        self.drawRadius = drawRadius
        self._autoMaxIter = autoMaxIter
        self.maxIterations = maxIterations
        self.escapeRadius = escapeRadius
        # Drawing and coloring configuration
        self.samples = samples
        self.blacknessLimit = blacknessLimit
        self._blackPixelCount = 0
        self.saturation = saturation
        self.coloringFunc = coloringFunc if coloringFunc is not None else IterativeColor
        self.drawer = self.GetDrawer()
        self.iterationHistogram = [0]*maxIterations
        self._totalIterations = 0
        self._updatedImage = False
        #configurate logging
        logging.basicConfig(format="%(levelname)s | %(module)s: %(message)s", level=logging.INFO)
    
    # DUNDER METHODS
    def __str__(self):
        return "<Mandelbrot object: (x={}, y={})>".format(self.x, self.y)

    def __repr__(self):
        return "<Mandelbrot object: (x={}, y={}), maxIterations={}, escapeRadius={}, coloringFunc={}>".format(
                                    self.x, self.y, self.maxIterations, self.escapeRadius, self.coloringFunc.__name__)

    # PROPERTIES
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value
        self.SetImageNotUpdated()

    @property
    def y(self):
        return self.__y
  
    @y.setter
    def y(self, value):
        self.__y = value
        self.SetImageNotUpdated()

    @property
    def drawRadius(self):
        return self._drawRadius
  
    @drawRadius.setter
    def drawRadius(self, value):
        self._drawRadius = value
        self.SetImageNotUpdated()

    @property
    def escapeRadius(self):
        return self._escapeRadius

    @escapeRadius.setter
    def escapeRadius(self, value):
        self._escapeRadius = value
        self.SetImageNotUpdated()

    @property
    def saturation(self):
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = value
        self.SetImageNotUpdated()

    @property
    def maxIterations(self):
        return self._maxIterations

    @maxIterations.setter
    def maxIterations(self, value):
        self._maxIterations = value
        self.iterationHistogram = [0]*self.maxIterations
        self.SetImageNotUpdated()

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = value
        self.drawer = self.GetDrawer()
        self.SetImageNotUpdated()

    # METHODS
    def GetDrawer(self):
        return CD(self.x-self.drawRadius, self.x+self.drawRadius,
                  self.y-self.drawRadius, self.y+self.drawRadius, 
                  self.samples, self.MandelbrotColor)

    def SetImageNotUpdated(self):
        try:
            self.drawer._updatedImage = False
        except AttributeError:
            logging.debug("Mandelbrot has no drawer attribute (yet). "+
                          "Can't set _updatedImage to false.")

    def GetIterations(self, cNum):
        tempResult = 0
        iterations = 0
        specialIters = 0
        for i in range(self.maxIterations):
            if (np.abs(tempResult) >= self.escapeRadius):
                if tempResult != 0:
                    specialIters = iterations + 1 - log2(np.abs(log(np.abs(tempResult))))
                return iterations, specialIters
            tempResult = tempResult**2 + cNum
            iterations += 1

        if tempResult != 0:
            specialIters = iterations + 1 - log2(np.abs(log(np.abs(tempResult))))
        return (iterations, specialIters)
    
    def GetAllPointIterations(self, points):
        iterationArr = np.empty([self.samples, self.samples], dtype=np.uint16)
        dtlIterationArr = np.empty([self.samples, self.samples], dtype=np.float32)
        rowCount = 0
        for row in points:
            pointCount = 0
            for point in row:
                if self.IsInMainCardioid(point):
                    iterationArr[rowCount, pointCount] = 0
                    dtlIterationArr[rowCount, pointCount] = 0
                else:
                    iterations, dtlIterations = self.GetIterations(point)
                    iterationArr[rowCount, pointCount] = iterations
                    dtlIterationArr[rowCount, pointCount] = dtlIterations
                    self._totalIterations += dtlIterations
                    if iterations != 0:
                        self.iterationHistogram[iterations-1] += dtlIterations
                pointCount += 1
            rowCount += 1
        return iterationArr, dtlIterationArr

    def IsInMainCardioid(self, point):
        x = point.real
        y = point.imag
        q = (x - 0.25)**2 + y**2
        return True if (q*(q+(x-0.25)) < 0.25*y**2) else False

    def ColorImage(self, iterationArr, dtlIterationArr, colorArr):
        self._blackPixelCount = 0
        rowCount = 0
        pointRGB = (0, 0, 0)
        for row in colorArr:
            pointCount = 0
            for point in row:
                pointIters = iterationArr[rowCount, pointCount]
                dtlPointIters = dtlIterationArr[rowCount, pointCount]
                # Add black as a color when the number inside the set.
                if pointIters == 0 or pointIters == self.maxIterations:
                    self._blackPixelCount += 1
                    pointRGB = (0, 0, 0)
                else:
                    pointRGB = self.coloringFunc(
                                                    iterations=pointIters, 
                                                    dtlIterations=dtlPointIters,
                                                    maxIterations=self.maxIterations, 
                                                    totalIterations=self._totalIterations,
                                                    histogram=self.iterationHistogram,
                                                    saturation=self.saturation)
                pointRGB = list(map(lambda x: 255*x, pointRGB))
                colorArr[rowCount, pointCount] = pointRGB
                pointCount += 1
            rowCount += 1

    def MandelbrotColor(self, points, colorArr):
        if self._autoMaxIter:
            self.maxIterations = self.FindOptimalMaxiter()
        iterationArr, dtlIterationArr = self.GetAllPointIterations(points)
        logging.debug("Generating mandelbrot image using coloring function: {}".format(self.coloringFunc.__name__))
        self.ColorImage(iterationArr, dtlIterationArr, colorArr)

    def GetBlackPixels(self, iterationArr, dtlIterationArr):
        self._blackPixelCount = 0
        rowCount = 0
        for row in iterationArr:
            pointCount = 0
            for point in row:
                pointIters = iterationArr[rowCount, pointCount]
                # Increment blackPixels, if the color will be black.
                if pointIters == 0 or pointIters == self.maxIterations:
                    self._blackPixelCount += 1
                pointCount += 1
            rowCount += 1

    def FindOptimalMaxiter(self, minVal=64, maxVal=1024, stepSize=32):
        #store current values
        maxIterStore, self.maxIterations = self.maxIterations, minVal
        sampleStore, self.samples = self.samples, 50
        colorFuncStore, self.coloringFunc  = self.coloringFunc, IterativeColor
        points = self.drawer.GetComplexNums()
        pixelCount = self.samples**2
        blackQuotient = 10
        while blackQuotient > self.blacknessLimit and self.maxIterations < maxVal:
            iterationArr, dtlIterationArr = self.GetAllPointIterations(points)
            self.GetBlackPixels(iterationArr, dtlIterationArr)
            blackCount = self._blackPixelCount
            blackQuotient = blackCount/pixelCount
            self.maxIterations += stepSize
        result = self.maxIterations
        # Reset properties to stored values.
        self.maxIterations = maxIterStore
        self.samples = sampleStore
        self.coloringFunc = colorFuncStore
        logging.info("Found optimal maxIterations value: {} || Black pixels: {}%.".format
                     (result, 100*blackQuotient))
        return result

    def show(self):
        logging.debug("Showing mandelbrot: " + repr(self))
        self.drawer.Plot()

    def SaveImg(self, filename, dpi=100):
        self.drawer.SaveFig(filename, dpi=dpi)
