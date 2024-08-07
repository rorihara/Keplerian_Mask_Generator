# make_KeplerianMask.py

This repository contains a Python script for generating Keplerian masks based to be used for CLEANing or moment map analysis. The script processes astronomical observation data to create masks for specific celestial objects' disks.

## How to Run

1. Install the required libraries.
2. Set the input parameters in the script.
3. Run the script.
   
```bash
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

You need to set several input parameters at the beginning of the script. These parameters control the behavior of the script and the nature of the output. Here is a detailed description of each parameter:

- `pd`: The file path to the directory containing the input data and where the output will be saved.
   - Example: '/path/to/parent/directory/'
- `cf`: A factor used to convolve the data. This parameter adjusts the smoothing applied to the data.
   - Example: 1.0 (beam size)
- `savefits`: A boolean flag indicating whether the generated mask should be saved as a FITS file.
   - Values: True (save the FITS file), False (do not save the FITS file, save as a npy file)
- `slice_data`: A boolean flag that determines if the data should be sliced. This is relevant only if savefits is set to False.
   - Values: True (slice the data), False (do not slice the data)
- `same_upperlower`: A boolean flag indicating whether the same parameters should be used for both the upper and lower surfaces of the disk.
   - Values: True (use the same parameters for both surfaces), False (use different parameters for each surface)
- `make_animation`: A boolean flag indicating whether an animation of the mask should be created. This is relevant only if savefits is set to False.
   - Values: True (create an animation), False (do not create an animation)
- `animation_velocityrange`: The velocity range for the animation, specified as a maximum value in km/s.
   - Example: 3 (create an animation for velocities from -3 km/s to 3 km/s)

## Disk Model

### Height of Emitting Surfaces

The height of the emitting surfaces is modeled using the following equation:

$$H = h_0 \left(\frac{r}{100\text{au}}\right)^p \exp\left[-\left(\frac{r}{R_b}\right)^q\right]$$

where:
- $h_0$ is a scaling factor for the height.
- $r$ is the radial distance from the center of the disk.
- $p$ and $𝑞$ are power-law exponents.
- $R_b$ is a characteristic radius beyond which the height drops off exponentially.

### Line Widths
The radial profile of the line width (Doppler parameter) is modeled using the following equation:

$$\Delta V = L_{0} \left(\frac{r}{100\text{au}}\right)^p \left(\frac{z}{100\text{au}}\right)^q $$

where:
- $L_{0}$ is a scaling factor for the line width.
- $r$ is the radial distance from the center of the disk.
- $z$ is the vertical distance from the midplane of the disk.
- $p$ and $q$ are power-law exponents.

### Author

Ryuta Orihara (roriharaiba@gmail.com)
