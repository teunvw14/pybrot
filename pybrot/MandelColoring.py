from colorsys import hsv_to_rgb

# This script provides some functions that can be used to determine 
# what color a point should be based on the iterations required to go over the escapeRadius value.

def IterativeColor(iterations, maxIterations, *args):
    hueQuotient = iterations/maxIterations
    H = hueQuotient
    S = 0.8
    V = 1
    return hsv_to_rgb(H, S, V)

def SmoothColor(iterations, maxIterations, totalIterations, detIterations, iterationHistogram, *args):
    hue = 0.0
    for i in range(iterations):
        hue += iterationHistogram[i]
    hue = hue/totalIterations
    H = detIterations**(1/4)
    S = 0.8
    V = 1
    return hsv_to_rgb(H, S, V)
