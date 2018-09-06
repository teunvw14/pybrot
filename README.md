# Pybrot
Pybrot is a python package that you can use to create images of the mandelbrot set like this:

![Picture of mandelbrot set goes here.](mandelbrots/mandelbrot_ex_2.png)

# Installation
This project is still currently in the python test package index. To install you can use:
`python -m pip install --index-url https://test.pypi.org/simple/ pybrot`

# Use

You can initialise a mandelbrot object like so:

`m = Mandelbrot()`

Then you can call

`m.Show()`

to show the image, or use

`m.SaveImg("Mandelbrot.png")`

to save it as an image.
