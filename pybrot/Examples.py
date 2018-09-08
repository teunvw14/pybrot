from pybrot.ComplexDraw import ComplexDraw as CD
from pybrot.Mandelbrot import Mandelbrot
from pybrot.MandelColoring import IterativeColor, SmoothColor

m = Mandelbrot(samples=500, escapeRadius=4, autoMaxIter=False)
m.Show()

m = Mandelbrot(-0.9230110468224410331799630273585336748656, 
                0.3103593603697618780906159981443973705961, 
                0.0001, maxIterations=32, samples=500, blacknessLimit=0.2, coloringFunc=SmoothColor)
m.Show()

m = Mandelbrot(samples=500)
m.SaveImg("test", dpi=500)

cd = CD()
cd.Plot()