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

$$H = h_0 \left(\frac{r}{100\text{au}}\right)^p \exp\left[-\left(\frac{r}{R_b}\right)^q\right]$$

where:
- $h_0$ is a scaling factor for the height.
- $r$ is the radial distance from the center of the disk.
- $p$ and $𝑞$ are power-law exponents.
- $R_b$ is a characteristic radius beyond which the height drops off exponentially.

### Radially Varying Line Widths

$$\Delta V = L_{w0} \left(\frac{r}{100\text{au}}\right)^p \left(\frac{z}{100\text{au}}\right)^q $$

where:
- $L_{w0}$ is a scaling factor for the line width.
- $r$ is the radial distance from the center of the disk.
- $z$ is the vertical distance from the midplane of the disk.
- $p$ and $q$ are power-law exponents.

### Author

Ryuta Orihara (roriharaiba@gmail.com)
