import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="sklearn_program_synthesis",
    version="0.1.0",
    author="Eddie Pantridge",
    author_email="erp12@hampshire.edu",
    description="A Sklearn compatible program synthesis framework.",
    license="LGPL",
    keywords=["push", "plushi", "genetic programming", "simulated annealing"],
    url="https://github.com/erp12/Pysh",
    packages=find_packages(exclude=['benchmark']),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        'Programming Language :: Python :: 3',
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ]
)
