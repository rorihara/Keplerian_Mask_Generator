from KeplerianMaskGenerator import generator as KMG

config = {
        'pd': '/path/to/directory/', # Path to parent directory of FITS file
        'fits':'xxx.fits', # Name of FITS file
        'cf': 1, # Convolution factor
        'same_upperlower': False, # whether or not to use the same upper and lower surface
        'slice_image': False, # whether or not to slice the image
        }

source = {
    'name':'source', # Source name
    'dpc':100., # Distance to the source (pc)
    'Ms':1., # Solar masses (Mo)
    'Vsys':5., # velocity of the system (km/s)
    'incl':30., # inclination (deg)
    'pa':30., # position angle (deg)
    'vel_sign':1, # 1 for clockwise, -1 for counterclockwise
    'Rout':100, # disk radius (au)
    'dRA':0., # offset in RA (arcsec)
    'dDEC':0., # offset in DEC (arcsec)
    'h0_u':30., # scaling factor for the height of the upper surface
    'p_u':1., # power law index of the upper surface
    'Rb_u':300., # break radius of the upper surface (au)
    'q_u':1., # tapering index of the upper surface
    'h0_l':30., # scaling factor for the height of the lower surface (if same_upperlower == False)
    'p_l':1., # power law index of the lower surface (if same_upperlower == False)
    'Rb_l':300., # break radius of the lower surface (au) (if same_upperlower == False)
    'q_l':1., # tapering index of the lower surface (if same_upperlower == False)
    'L0':0.3, # linewidth at 100 au (km/s)
    'p':-0.5, # power law index for the linewidth as a function of radius
    'q':-0.5 # power law index for the linewidth as a function of height
    }

# Gnerate the masks
kmg = KMG(config, source)

# Save the masks
kmg.save_mask(save_fits=True, save_npy=True, save_animation=True, vrange=3) # vrange: the velocity range for animation (e.g., -3 km/s to 3 km/s)

# Optional ====================================================

# Retrieve the processed data and masks from the KMG instance
data = kmg.data # The original or sliced image array.
ra = kmg.ra # The right ascension (RA) list.
dec = kmg.dec # The declination (DEC) list.
vel = kmg.vel # The Vlsr list (km/s).
all_mask = kmg.all_mask # A boolean array that combines both the upper surface and lower surface masks.
upper_mask = kmg.upper_mask # A boolean array representing only the upper surface mask.
lower_mask = kmg.lower_mask # A boolean array representing only the lower surface mask.

# If using the mask in CASA, convert the FITS to CASA format.
# In CASA
# fitsimage = 'xxx_keplerianmask.fits'
# importfits(fitsimage = fitsimage, imagename = fitsimage.split('.fits')[0]+'.image', overwrite = True)
