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
pip install numpy matplotlib astropy opencv-python
```

## Input Parameters

You need to set several input parameters at the beginning of the script.

- pd: Path to the parent directory
-- Description: The file path to the directory containing the input data and where the output will be saved.
-- Example: /path/to/parent/directory
- cf: Convolution factor
-- Description: A factor used to convolve the data. This parameter adjusts the smoothing applied to the data.
-- Example: 1.0 (no convolution), 0.5 (half the original resolution)
- savefits: Whether to save the FITS file or not
-- Description: A boolean flag indicating whether the generated mask should be saved as a FITS file.
-- Values: True (save the FITS file), False (do not save the FITS file)
- slice_data: Whether to slice the data or not (if savefits is False)
-- Description: A boolean flag that determines if the data should be sliced. This is relevant only if savefits is set to False.
-- Values: True (slice the data), False (do not slice the data)
- same_upperlower: Whether to use the same upper and lower surface or not
-- Description: A boolean flag indicating whether the same parameters should be used for both the upper and lower surfaces of the disk.
-- Values: True (use the same parameters for both surfaces), False (use different parameters for each surface)
- make_animation: Whether to make an animation or not (if savefits is False)
-- Description: A boolean flag indicating whether an animation of the mask should be created. This is relevant only if savefits is set to False.
-- Values: True (create an animation), False (do not create an animation)
- animation_velocityrange: Velocity range (km/s) for the animation
-- Description: The velocity range for the animation, specified as a tuple of minimum and maximum values in km/s.
-- Example: (-5, 5) (create an animation for velocities from -5 km/s to 5 km/s)


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

### Line Widths

$$\Delta V = L_{0} \left(\frac{r}{100\text{au}}\right)^p \left(\frac{z}{100\text{au}}\right)^q $$

where:
- $L_{0}$ is a scaling factor for the line width.
- $r$ is the radial distance from the center of the disk.
- $z$ is the vertical distance from the midplane of the disk.
- $p$ and $q$ are power-law exponents.

### Author

Ryuta Orihara (roriharaiba@gmail.com)
