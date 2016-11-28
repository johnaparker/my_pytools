import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "my_pytools",
    version = "0.1.0",
    author = "John Parker",
    author_email = "japarker@uchicago.com",
    description = ("My Python helper library"),
    license = "MIT",
    keywords = "Python",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['my_pytools'],
    # modules=['my_matplotlib'],
    # subpackages=['my_matplotlib'],
    install_requires=['numpy', 'scipy', 'matplotlib'],
    include_package_data = True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
    ],
)
