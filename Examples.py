from ComplexDraw import ComplexDraw as CD
from Mandelbrot import Mandelbrot

m = Mandelbrot()
m.Show()

m = Mandelbrot(-0.9230110468224410331799630273585336748656, 
                0.3103593603697618780906159981443973705961, 
                0.0001, maxIterations=32, samples=100, blacknessLimit=0.1)
m.Show()

m = Mandelbrot(samples=500)
m.SaveImg("test", dpi=500)

cd = CD()
cd.Plot()