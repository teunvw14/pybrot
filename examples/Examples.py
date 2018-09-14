from pybrot.ComplexDraw import ComplexDraw as CD
from pybrot.Mandelbrot import Mandelbrot
from pybrot.MandelColoring import IterativeColor, SmoothColor, HistoColor, FourthRootColor, GrayScaleColor

m = Mandelbrot()
m.show()

m = Mandelbrot(coloringFunc=GrayScaleColor,
               autoMaxIter=False, maxIterations=32)
m.show()

m = Mandelbrot(-0.9230110468224410331799630273585336748656, 
                0.3103593603697618780906159981443973705961, 
               0.00001, samples=250, blacknessLimit=0.2, coloringFunc=HistoColor)
m.show()

m = Mandelbrot(autoMaxIter=False, maxIterations=128, samples=1500, drawRadius=1.5)
m.SaveImg("test", dpi=500)

cd = CD(samples=500)
cd.Plot()   
