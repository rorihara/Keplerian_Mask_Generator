from KeplerianMaskGenerator import generator as KMG

config = {
        'pd': '/Volumes/Extreme_SSD/obs_data/ALMA/MAPS/HD163296/casa_space/', # Path to parent directory of FITS file
        'fits':'test.fits', # Name of FITS file
        'cf': 1, # Convolution factor
        'same_upperlower': False, # whether to use the same upper and lower surface or not
        }

source = {
    'name':'HD_163296', # Source name
    'dpc':101.5, # Distance to the source (pc)
    'Ms':1.92, # Solar masses (Mo)
    'Vsys':5.76, # velocity of the system (km/s)
    'incl':-46.7, # inclination (deg)
    'pa':312.8, # position angle (deg)
    'vel_sign':-1, # 1 for clockwise, -1 for counterclockwise
    'Rout':550, # disk radius (au)
    'dRA':0.01267, # offset in RA (arcsec)
    'dDEC':0.00295, # offset in DEC (arcsec)
    'h0_u':29.6, # scaling factor for the height of the upper surface
    'p_u':1.29, # power law index of the upper surface
    'Rb_u':435.4, # break radius of the upper surface (au)
    'q_u':1.66, # tapering index of the upper surface
    'h0_l':16.7, # scaling factor for the height of the lower surface (if same_upperlower == False)
    'p_l':1.16, # power law index of the lower surface (if same_upperlower == False)
    'Rb_l':559.0, # break radius of the lower surface (au) (if same_upperlower == False)
    'q_l':3.5, # tapering index of the lower surface (if same_upperlower == False)
    'L0':0.32, # linewidth at 100 au (km/s)
    'p':-0.2, # power law index for the linewidth as a function of radius
    'q':-0.47 # power law index for the linewidth as a function of height
    }

# Initialize the generator
kmg = KMG(config, source)
# Gnerate the masks
mask_arrays = kmg.generate_mask(slice_image=False) # outputs: (upper surface, lower surface, upper + lower surface)
# Save the masks
kmg.save_outputs(save_fits=True, save_npy=True, save_animation=True, vrange=3) # vrange: the velocity range for animation (e.g., -3 km/s to 3 km/s)

