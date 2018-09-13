from colorsys import hsv_to_rgb

# This script provides some functions that can be used to determine 
# what color a point should be based on the iterations required to go over the escapeRadius value.

def IterativeColor(*args, **kwargs):
    iterations = kwargs["iterations"]
    maxIterations = kwargs["maxIterations"]
    hueQuotient = iterations/maxIterations
    H = hueQuotient
    S = kwargs["saturation"]
    V = 1
    return hsv_to_rgb(H, S, V)

def HistoColor(*args, **kwargs):
    iterations = kwargs["iterations"]
    iterationHistogram = kwargs["histogram"]
    totalIterations = kwargs["totalIterations"]
    hue = 0.0
    for i in range(iterations):
        hue += iterationHistogram[i]
    hue = hue/totalIterations
    H = hue
    S = kwargs["saturation"]
    V = 1
    return hsv_to_rgb(H, S, V)

def SmoothColor(*args, **kwargs):
    dtlIterations = kwargs["dtlIterations"]
    maxIterations = kwargs["maxIterations"]
    # detIterations is sometimes larger than maxIterations by a small margin.
    hue = dtlIterations / (maxIterations ** 1.5)
    H = hue
    S = kwargs["saturation"]
    V = 1
    return hsv_to_rgb(H, S, V)

def FourthRootColor(*args, **kwargs):    
    dtlIterations = kwargs["dtlIterations"]
    H = dtlIterations**(0.25)
    S = kwargs["saturation"]
    V = 1
    return hsv_to_rgb(H, S, V)

def GrayScaleColor(*args, **kwargs):
    iterations = kwargs["iterations"]
    maxIterations = kwargs["maxIterations"]
    hueQuotient = (iterations/maxIterations)**(1/2)
    r, g, b = hueQuotient, hueQuotient, hueQuotient
    return (r, g, b)
