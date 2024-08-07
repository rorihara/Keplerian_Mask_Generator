pd = 'path/to/parent' #path to parent directory
cf = 1 #convolution factor
savefits = False # whether to save the fits or not
slice_data = False # whether to slice the data or not (if savefits == False)
same_upperlower = False # whether to use the same upper and lower surface or not
make_animation = True # whether to make an animation or not (if savefits == False)
animation_velocityrange = 3 # velocity range (km/s) for the animation

source = {
    'name':'source', # Source name
    'fits':'xxx.fits', # Fits file
    'dpc':100, # Distance to the source (pc)
    'Mstar':1.0, # Solar masses (Mo)
    'vsys':5.0, # velocity of the system (km/s)
    'incl':30, # inclination (deg)
    'pa':30, # position angle (deg)
    'vel_sign':1, # 1 for counterclockwise, -1 for clockwise
    'Rout':500, # disk radius (au)
    'dRA':0.0, # offset in RA (arcsec)
    'dDEC':0.0, # offset in DEC (arcsec)
    'h0_u':30, # scaling factor for the height of the upper surface
    'p_u':1.0, # power law index of the upper surface
    'Rb_u':300, # break radius of the upper surface (au)
    'q_u':1.0, # tapering index of the upper surface
    'h0_l':30, # scaling factor for the height of the lower surface (if same_upperlower == False)
    'p_l':1.0, # power law index of the lower surface (if same_upperlower == False)
    'Rb_l':300, # break radius of the lower surface (au) (if same_upperlower == False)
    'q_l':1.0, # tapering index of the lower surface (if same_upperlower == False)
    'L0':0.5, # linewidth at 100 au (km/s)
    'p':-0.5, # power law index for the linewidth as a function of radius
    'q':-0.1 # power law index for the linewidth as a function of height
    }
