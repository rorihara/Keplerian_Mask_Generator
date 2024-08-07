# keplerian_mask_generator.py

This tool generates Keplerian masks for astronomical data, optionally saves them in FITS or NPY formats, and creates animations of the data with overlaid masks. It is designed to handle FITS files and allows customization of various parameters related to the disk properties.

## How to Run

1. Install the required libraries.
2. Set the input parameters in the script.
3. Run the script.

```bash
python make_KeplerianMask.py
```

## Required Libraries

To run this script, you need the following Python libraries:

- Python 3.x
- `numpy`
- `matplotlib`
- `astropy`
- `cv2` (OpenCV)

Install the required libraries using the following command:
```bash
pip install numpy matplotlib astropy opencv-python
```

## Input Parameters

You need to set several input parameters at the beginning of the script. These parameters control the behavior of the script and the nature of the output. Here is a detailed description of each parameter and the corresponding dictionary key:

- `pd`:
   - *Description*: File path to the directory containing the input data and where the output will be saved.
   - *Example*: '/path/to/parent/directory/'
- `cf`:
   - *Description*: Factor used to convolve the data. This parameter adjusts the smoothing applied to the data.
   - *Example*: 1.0 (beam size)
- `savefits`:
   - *Description*: Boolean flag indicating whether the generated mask should be saved as a FITS file.
   - *Values*: True (save the FITS file), False (do not save the FITS file, save as a npy file)
- `slice_data`:
   - *Description*: Boolean flag that determines if the data should be sliced. This is relevant only if savefits is set to False.
   - *Values*: True (slice the data), False (do not slice the data)
- `same_upperlower`:
   - *Description*: Boolean flag indicating whether the same parameters should be used for both the upper and lower surfaces of the disk.
   - *Values*: True (use the same parameters for both surfaces), False (use different parameters for each surface)
- `make_animation`:
   - *Description*: Boolean flag indicating whether an animation of the mask should be created. This is relevant only if savefits is set to False.
   - *Values*: True (create an animation), False (do not create an animation)
- `animation_velocityrange`:
   - *Description*: Velocity range for the animation, specified as a maximum value in km/s.
   - *Example*: 3 (create an animation for velocities from -3 km/s to 3 km/s)

### Disk Model
The source dictionary contains the following parameters:

#### Basic Information
- `['name']`: Source name.
- `['fits']`: Name of the FITS file.
- `['dpc']`: Distance to the source in pc.
- `['Mstar']`: Mass of the central star in solar masses.
- `['vsys']`: Systemic velocity of the disk in km/s.
- `['incl']`: Inclination angle of the disk in degrees.
- `['pa']`: Position angle of the disk in degrees.
- `['vel_sign']`: Sign of the velocity (1 for approaching, -1 for receding).
- `['Rout']`: Outer radius of the disk in au.

#### Height of Emitting Surfaces

The height of the emitting surfaces is modeled using the following equation:

$$H = h_0 \left(\frac{r}{100\text{au}}\right)^p
\exp\left[-\left(\frac{r}{R_b}\right)^q\right]$$

where:
- $h_0$ is a scaling factor for the height. (Dictionary Key: `['h0_u']`, `['h0_l']`)
- $r$ is the radial distance from the center of the disk.
- $p$ is power law index for the surfaces. (Dictionary Key: `['p_u']`, `['p_l']`)
- $q$ is tapering index for the surfaces. (Dictionary Key: `['q_u']`, `['q_l']`)
- $R_b$ is a characteristic radius beyond which the height drops off exponentially. (Dictionary Key: `['Rb_u']`, `['Rb_l']`)

#### Line Widths
The profile of the line width (Doppler parameter) is modeled using the following equation:

$$\Delta V = L_{0} \left(\frac{r}{100\text{au}}\right)^p
\left(\frac{z}{100\text{au}}\right)^q $$

where:
- $L_{0}$ is a scaling factor for the line width. (Dictionary Key: `['L0']`)
- $r$ is the radial distance from the center of the disk.
- $z$ is the vertical distance from the midplane of the disk.
- $p$ and $q$ are the power law indices for the linewidth as functions of radius and height, respectively. (Dictionary Keys: `['p']`, `['q']`)

## Output
- If `savefits` is True, the masks will be saved as a FITS file.
- If `savefits` is False, the masks will be saved as a npy file.
- If `make_animation` is True, an animation will be created and saved as an HTML file.

### Author
Ryuta Orihara (roriharaiba@gmail.com)
