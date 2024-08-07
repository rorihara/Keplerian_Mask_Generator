# make_KeplerianMask.py

A script to build a Keplerian mask based to be used for CLEANing or moment map analysis. This will grab the image properties (axes, beam properties and so on) from the provide CASA image.

## Basic Usage

First, load up the function into the CASA instance:

```python
python make_keplerianmask.py
```

### Radially Varying Line Widths

With higher spatial resolutions it is possible to resolve the radially changing line width of emission lines. This manifests as a change in the width of the emission pattern as a function of radius. We assume that the radial profile of the line width (here we are describing the Doppler parameter, so a factor of 1.665 times smaller than the FWHM, is well described by a powerlaw,

![alt text](https://latex.codecogs.com/gif.latex?\Delta&space;V&space;(r)&space;=&space;\Delta&space;V_{0}&space;\times&space;\left(&space;\frac{r}{1^{\prime\prime}}&space;\right)^{\Delta&space;V_q} "Equation 1")

### Author

Written by Ryuta Orihara (roriharaiba@gmail.com), 2024.
