# KeplerianMaskGenerator

This tool generates Keplerian masks for data cubes of protoplanetary disks, optionally saves them in FITS or NPY formats, and creates animations of the data with overlaid masks. It is designed to handle FITS files and allows customization of various parameters related to the disk properties.

## How to Use

1. To install the package, run:
```bash
git clone https://github.com/andizq/discminer.git
cd Keplerian_Mask_Generator
pip install .
```
2. After installation, please run the script as shown in `example_run.py`.


## Required Libraries

To run this script, you need the following Python libraries:

- Python 3.x
- `numpy`
- `matplotlib`
- `astropy`
- `cv2` (OpenCV)

These libraries will also be installed automatically when you install this package.

## Input Parameters

### Config parameters
The config dictionary contains the following parameters:

- `pd`:
   - *Description*: Path to the directory containing the input FITS file.
   - *Example*: '/path/to/parent/directory/'
- `fits`:
   - *Description*: Name of the FITS file.
   - *Example*: 'xxx.fits'
- `cf`:
   - *Description*: Factor used to convolve the data. This parameter adjusts the smoothing applied to the data.
   - *Example*: 1.0 (beam size)
- `same_upperlower`:
   - *Description*: Boolean flag indicating whether the same parameters should be used for both the upper and lower surfaces of the disk.
   - *Values*: True (use the same parameters for both surfaces), False (use different parameters for each surface)

### Generate options

- `slice_image`:
   - *Description*: Boolean flag that determines if the image should be sliced. This is relevant only if savefits is set to False.
   - *Values*: True (slice the data), False (do not slice the data)
- `save_fits`:
   - *Description*: Boolean flag indicating whether the generated mask should be saved as a FITS file. This is relevant only if slice_image is set to False.
   - *Values*: True (save the FITS file), False (do not save the FITS file)
- `save_npy`:
   - *Description*: Boolean flag indicating whether the generated mask should be saved as a NPY file.
   - *Values*: True (save the NPY file), False (do not save the NPY file)
- `save_animation`:
   - *Description*: Boolean flag indicating whether an animation of the mask should be created. 
   - *Values*: True (create an animation), False (do not create an animation)
- `vrange`:
   - *Description*: Velocity range for the animation, specified as a maximum value in km/s. This is relevant only if save_animation is set to True.
   - *Example*: 3 (create an animation for velocities from -3 km/s to 3 km/s)

### Source parameters
The source dictionary contains the following parameters:

#### Basic Information
- `['name']`: Source name.
- `['dpc']`: Distance to the source (pc).
- `['Ms']`: Mass of the central star in solar masses.
- `['Vsys']`: Systemic velocity of the disk (km/s).
- `['incl']`: Inclination angle of the disk (deg).
- `['pa']`: Position angle of the disk (deg).
- `['vel_sign']`: Sign of the velocity (1 for clockwise, -1 for counterclockwise).
- `['Rout']`: Outer radius of the disk (au).
- `['dRA']`: Offset in RA (arcsec).
- `['dDEC']`: Offset in DEC (arcsec).

#### Height of Emitting Surfaces

The height of the emitting surfaces is modeled using the following equation:

$$h = h_0 \left(\frac{r}{100\text{au}}\right)^p
\exp\left[-\left(\frac{r}{R_b}\right)^q\right]$$

where:
- $h_0$ is a scaling factor for the height. (Dictionary Key: `['h0_u']`, `['h0_l']`)
- $r$ is the radial distance from the center of the disk.
- $p$ is power law index for the surfaces. (Dictionary Key: `['p_u']`, `['p_l']`)
- $q$ is tapering index for the surfaces. (Dictionary Key: `['q_u']`, `['q_l']`)
- $R_b$ is a characteristic radius beyond which the height drops off exponentially. (Dictionary Key: `['Rb_u']`, `['Rb_l']`)

#### Line Widths
The profile of the line width is modeled using the following equation:

$$\Delta V = L_{0} \left(\frac{r}{100\text{au}}\right)^p
\left(\frac{h}{100\text{au}}\right)^q $$

where:
- $L_{0}$ is a scaling factor for the line width. (Dictionary Key: `['L0']`)
- $r$ is the radial distance from the center of the disk.
- $h$ is the height of the emitting surface.
- $p$ and $q$ are the power law indices for the linewidth as functions of radius and height, respectively. (Dictionary Keys: `['p']`, `['q']`)

## Output
- If `savefits` is True, the masks are saved as a FITS file. If you use a mask in CASA, please convert it to CASA image format using the `importfits` task in the CASA tools before applying it. If the number of axes in the FITS data is four, they are ordered as [RA, DEC, STOKES, FREQ].
- If `savefits` is False, the masks will be saved as a npy file.
- If `make_animation` is True, an animation will be created and saved as an HTML file.

### Author
Ryuta Orihara (email: roriharaiba@gmail.com)
