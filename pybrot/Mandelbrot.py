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
        self.saturation = saturation
        self.coloringFunc = coloringFunc if coloringFunc is not None else IterativeColor
        self.drawer = self.GetDrawer()
        self.iterationHistogram = [0]*maxIterations
        self.totalIterations = 0
        #configurate logging
        logging.basicConfig(format="%(levelname)s | %(module)s: %(message)s", level=logging.DEBUG)
    
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

    @property
    def y(self):
        return self.__y
  
    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def drawRadius(self):
        return self._drawRadius
  
    @drawRadius.setter
    def drawRadius(self, value):
        self._drawRadius = value
    
    @property
    def escapeRadius(self):
        return self._escapeRadius

    @escapeRadius.setter
    def escapeRadius(self, value):
        self._escapeRadius = value

    @property
    def saturation(self):
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = value

    @property
    def maxIterations(self):
        return self._maxIterations

    @maxIterations.setter
    def maxIterations(self, value):
        self._maxIterations = value
        self.iterationHistogram = [0]*self.maxIterations

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = value
        self.drawer = self.GetDrawer()

    # METHODS
    def GetDrawer(self):
        return CD(self.x-self.drawRadius, self.x+self.drawRadius,
                  self.y-self.drawRadius, self.y+self.drawRadius, 
                  self.samples, self.MandelbrotColor)

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
        intIterationArr = []
        dtlIterationArr = []
        for row in points:
            for point in row:
                if self.IsInMainCardioid(point):
                    intIterationArr.append(0)
                    dtlIterationArr.append(0)
                else:
                    iterations, dtlIterations = self.GetIterations(point)
                    intIterationArr.append(iterations)
                    dtlIterationArr.append(dtlIterations)
                    self.totalIterations += dtlIterations
                    if iterations != 0:
                        self.iterationHistogram[iterations-1] += dtlIterations
        return intIterationArr, dtlIterationArr

    def IsInMainCardioid(self, point):
        x = point.real
        y = point.imag
        q = (x - 0.25)**2 + y**2
        return True if (q*(q+(x-0.25)) < 0.25*y**2) else False

    def GenerateRows(self, points, iterArr, detIterArr):
        iterationArrCounter = 0
        for row in points:
            rowBlackCount = 0
            tempRow = []
            for point in row:
                pointIters = iterArr[iterationArrCounter]
                dtlPointIters = detIterArr[iterationArrCounter]
                # Add black as a color when the number inside the set.
                if pointIters == 0 or pointIters == self.maxIterations:
                    rowBlackCount += 1
                    tempRow.append((0,0,0))
                else:
                    tempRow.append(self.coloringFunc(
                                                    iterations=pointIters, 
                                                    dtlIterations=dtlPointIters,
                                                    maxIterations=self.maxIterations, 
                                                    totalIterations=self.totalIterations,
                                                    histogram=self.iterationHistogram,
                                                    saturation=self.saturation))
                iterationArrCounter += 1
            yield (tempRow, rowBlackCount)

    def MandelbrotColor(self, points):
        mbColorArr = []
        if self._autoMaxIter:
            self.maxIterations = self.FindOptimalMaxiter()
        iterationArr, dtlIterationArr = self.GetAllPointIterations(points)
        logging.debug("Generating mandelbrot image using coloring function: {}".format(self.coloringFunc.__name__))
        for row in self.GenerateRows(points, iterationArr, dtlIterationArr):
            mbColorArr.append(row[0])
        return mbColorArr

    def FindOptimalMaxiter(self, minVal=64, maxVal=1024, stepSize=32):
        maxIterStore, self.maxIterations = self.maxIterations, minVal
        sampleStore, self.samples = self.samples, 50
        colorFuncStore, self.coloringFunc  = self.coloringFunc, IterativeColor
        points = self.drawer.GetComplexNums()
        mbColorArr = []
        blackQuotient = 10
        while blackQuotient > self.blacknessLimit and self.maxIterations < maxVal:
            mbColorArr = []
            pixelCount = 0
            blackCount = 0
            iterationArr, dtlIterationArr = self.GetAllPointIterations(points)
            for row in self.GenerateRows(points, iterationArr, dtlIterationArr):
                mbColorArr.append(row[0])
                pixelCount += len(row[0])
                blackCount += row[1]
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

    def Show(self):
        logging.debug("Showing mandelbrot: " + repr(self))
        self.drawer.Plot()

    def SaveImg(self, filename, dpi=100):
        self.drawer.SaveFig(filename, dpi=dpi)
