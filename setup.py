import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybrot",
    version="0.0.1",
    author="Teun van Wezel",
    author_email="vanwezelteun@gmail.com",
    description="A python package to create mandelbrot set images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teunvw14/pybrot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
