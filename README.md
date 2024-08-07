# make_KeplerianMask.py

This repository contains a Python script for generating Keplerian masks based to be used for CLEANing or moment map analysis. The script processes astronomical observation data to create masks for specific celestial objects' disks.

## How to Run

1. Install the required libraries.
2. Set the input parameters in the script.
3. Run the script.
   
```python
python make_KeplerianMask.py
```

## Required Libraries

To run this script, you need the following Python libraries:
- `numpy`
- `matplotlib`
- `astropy`
- `cv2` (OpenCV)

Install the required libraries using the following command:
```bash
pip install numpy matplotlib astropy opencv-python scipy
```

## Input Parameters

You need to set several input parameters at the beginning of the script.

- `pd`: Path to the parent directory
- `cf`: Convolution factor
- `savefits`: Whether to save the FITS file or not
- `slice_data`: Whether to slice the data or not (if `savefits` is `False`)
- `same_upperlower`: Whether to use the same upper and lower surface or not
- `make_animation`: Whether to make an animation or not (if `savefits` is `False`)
- `animation_velocityrange`: Velocity range (km/s) for the animation


## Output

- If `savefits` is `True`, the generated mask will be saved as a FITS file.
- If `make_animation` is `True`, an animation will be created for the specified velocity range.

## Disk Model

### Height of Emitting Surfaces

$$H = h_0 \left(\frac{r}{100\text{au}}\right)^p \exp\left(-\left(\frac{r}{R_b}\right)^q\right)$$

### Radially Varying Line Widths

With higher spatial resolutions it is possible to resolve the radially changing line width of emission lines. This manifests as a change in the width of the emission pattern as a function of radius. We assume that the radial profile of the line width (here we are describing the Doppler parameter, so a factor of 1.665 times smaller than the FWHM, is well described by a powerlaw,

$$\Delta V = L_{w0} \left(\frac{r}{100\text{au}}\right)^p \left(\frac{z}{100\text{au}}\right)^q $$

### Author

Ryuta Orihara (roriharaiba@gmail.com)
