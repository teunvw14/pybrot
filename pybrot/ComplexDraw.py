import logging
import numpy as np
import matplotlib.pyplot as plt
from numpy import add, subtract, divide, multiply, mod, sin, cos, angle, log, log2, pi
from matplotlib.colors import hsv_to_rgb
from colorsys import hls_to_rgb

class ComplexDraw:
    def __init__(self, xmin=-10, xmax=10, ymin=-10, ymax=10, samples=500, ColorFunc=None):
        #plot settings
        self._samples = samples
        #ranges for the axes
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax
        #define the coloring function
        self.ColorFunc = ColorFunc if ColorFunc is not None else self.DomainColoringColorFunc
        #create domain
        self.CreateDomain()

        self.colorArr = []
        #configurate logging
        logging.basicConfig(format="%(levelname)s | %(module)s: %(message)s", level=logging.DEBUG)

    # This is a function to create an array of points representing an x, y plane.
    def CreateDomain(self):
        x = np.linspace(self._xmin, self._xmax, self._samples)
        y = np.linspace(self._ymin, self._ymax, self._samples)
        self.xx, self.yy=np.meshgrid(x,y)

    # This is the default coloring function. It is a good example for what this program might be used for.
    def DomainColoringColorFunc(self, cNums, a=0.9):
        # This function calculates a color based on some of the attributes associated with each complex number.
        # For more information on domain coloring see: https://en.wikipedia.org/wiki/Domain_coloring
        dcolorArray = []
        for row in cNums:
            tempRow = []
            for c in row:
                H = angle(c)
                L = (1 - a**(np.abs(c)))
                S = 1
                rgb = hls_to_rgb(H, L, S)
                tempRow.append(rgb)
            dcolorArray.append(tempRow)
        return dcolorArray

    def GetComplexNums(self):
        return self.z(self.xx, self.yy)

    # Function to get the color corresponding to each point.
    def GetColours(self):
        self.colorArr = self.ColorFunc(self.GetComplexNums())

    # This function shows the created plot of the complex plane.
    def Plot(self):
        if self.colorArr == []:
            self.CreateImage()
        plt.show()

    def CreateImage(self):
        self.GetColours()
        plt.imshow(self.colorArr)
        #Hide x and y axes
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)
    
    def SaveFig(self, filename, dpi=100):
        if self.colorArr == []:
            self.CreateImage()
        # Save without white borders.
        logging.info("Saving plot of complex plane in file {}.".format(filename))
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, dpi=dpi)

    def z(self, x, y):
        return x + 1j*y
