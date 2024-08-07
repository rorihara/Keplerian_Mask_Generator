import os
import numpy as np
import matplotlib.pyplot as plt
import astropy.constants as C
import astropy.units as U
import astropy.io.fits as FITS
import cv2
from matplotlib.animation import FuncAnimation
from matplotlib.animation import HTMLWriter

# Input parameters ###########################################################
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
    'z0_u':30, # height of the upper surface at 100 au
    'p_u':1.0, # power of the upper surface
    'Rb_u':300, # break radius of the upper surface (au)
    'q_u':1.0, # taper of the upper surface
    'z0_l':30, # height of the lower surface at 100 au (if same_upperlower == False)
    'p_l':1.0, # power of the lower surface (if same_upperlower == False)
    'Rb_l':300, # break radius of the lower surface (au) (if same_upperlower == False)
    'q_l':1.0, # taper of the lower surface (if same_upperlower == False)
    'Lw0':0.5, # linewidth at 100 au (km/s)
    'p':-0.5, # power of the lineprofile (r)
    'q':-0.1 # power of the lineprofile (z)
    }
################################################################################

# Check if fits will be saved
if savefits == True:
    slice_data = False
    make_animation = False
    savefitsname = source['fits'].split('.fits')[0]+'_keplerianmask.fits'
    os.system('rm '+pd+savefitsname)
    os.system('cp '+pd+source['fits']+' '+pd+savefitsname)

# Constants and units
G = C.G.cgs.value # Gravitational constant in cgs units (cm^3 g^-1 s^-2)
clight = C.c.cgs.value # Speed of light in cgs units (cm s^-1)
deg2arcsec = (U.deg).to(U.arcsec)  # deg to arcsec
au2cm = (U.au).to(U.cm) # au to cm
km2cm = (U.km).to(U.cm) # km to cm

# Rotation matrix
def rot(i, p): 
    i, p = np.radians(i), np.radians(p)
    ci, si = np.cos(i), np.sin(i)
    cp, sp = np.cos(p), np.sin(p)
    return np.array([[cp, -sp * ci, -sp * si], [sp, cp * ci, cp * si], [0, -si, ci]])

# Surface of the disk
def z_surf(r, z0, p, Rb, q, R=100):
    return z0*(r/R)**p * np.exp(-(r/Rb)**q)

# Linewidth
def linewidth(r, z, Lw0, p, q):
    return Lw0 * (r/100)**p * (z/100)**q

# Circulate kernel for beam convolution
def circular_kernel(beam_pix):
    L = np.arange(-round(beam_pix/2), round(beam_pix/2) + 1)
    X, Y = np.meshgrid(L, L)
    kernel = (X**2 + Y**2) <= round(beam_pix/2)**2
    return kernel.astype(np.uint8)

# Dilate masks to make them thicker
def dilate_masks(masks, kernel):
    return [cv2.dilate(mask.astype(np.uint8), kernel, iterations=1) for mask in masks]

print('Source: '+source['name'])

# Load fits
fitsfile = pd + source['fits']
with FITS.open(fitsfile) as hdu:
    header = hdu[0].header
    if header['NAXIS'] == 4: data = hdu[0].data[0]
    elif header['NAXIS'] == 3: data = hdu[0].data
    pix = header['CDELT2'] * deg2arcsec # Pixel size
    imsize = header['NAXIS1'] # Image size
    beam = header['BMAJ'] * deg2arcsec
    imc = int(imsize / 2) # Image center
    indlist = np.arange(0, imsize)
    ra = -(indlist - imc) * pix
    dec = (indlist - imc) * pix
    restfreq = header['RESTFRQ'] # Rest frequency
    cw = np.abs(header['CDELT3']*clight/restfreq)/km2cm # Channel width in km/s

# Load source params
M = source['Mstar'] * (U.M_sun).to(U.g) 
dpc = source['dpc']
Rmax = source['Rout']
Vsys = source['vsys']
drot = source['vel_sign']
incl = source['incl']
pa = source['pa']

# Slice data (space)
if slice_data == True:
    slice_arcsec = int(round(Rmax / dpc)) + 1
    ras = np.argmin((ra - slice_arcsec) ** 2)
    rae = np.argmin((ra + slice_arcsec) ** 2) + 1
    decs = np.argmin((dec + slice_arcsec) ** 2)
    dece = np.argmin((dec - slice_arcsec) ** 2) + 1
    ra = ra[ras:rae]
    dec = dec[decs:dece]
    data = data[:, decs:dece, ras:rae]
print('Data shape: '+str(data.shape))
print('Making keplerian masks...', end='', flush=True)

# Convert pix to grid
grid_ra = np.append(ra+pix/2, np.min(ra-pix/2))
grid_dec = np.append(dec-pix/2, np.max(dec+pix/2))

# Load velocity axis
f_start = header['CRVAL3'] # frequency of the first channel
df = header['CDELT3'] # channel width
nf = header['NAXIS3'] # number of channels
f_list = np.linspace(f_start, f_start+df*nf, nf)
vel_list = clight*(restfreq-f_list)/restfreq/km2cm
vel_list_vsys = vel_list - Vsys
chan_top = np.argmin(np.abs(vel_list_vsys - animation_velocityrange))
chan_bottom = np.argmin(np.abs(vel_list_vsys + animation_velocityrange))

# Create keplerian mask
# Base vectors
no = rot(incl, pa)[:, 2] # normal vector of the disk midplane
ez = rot(0, 0)[:, 2] # z-axis vector (line of sight)
lo = np.cross(no, ez); lo /= np.linalg.norm(lo)
mo = np.cross(no, lo)
base_o = (lo, mo, no) # base vectors

# Surface coordinates
R_list = np.arange(0, Rmax+pix*dpc/2, pix*dpc/2)[1:]
t_list = np.arange(0, 2*np.pi, pix*dpc/Rmax/2)
R, t = np.meshgrid(R_list, t_list) 
Z_u = z_surf(R, source['z0_u'], source['p_u'], source['Rb_u'], source['q_u'])
if same_upperlower == True: Z_l = Z_u
else: Z_l = z_surf(R, source['z0_l'], source['p_l'], source['Rb_l'], source['q_l'])

Sux = R*(np.cos(t)*lo[0] + np.sin(t)*mo[0]) + Z_u*no[0]
Suy = R*(np.cos(t)*lo[1] + np.sin(t)*mo[1]) + Z_u*no[1]
Slx = R*(np.cos(t)*lo[0] + np.sin(t)*mo[0]) - Z_l*no[0]
Sly = R*(np.cos(t)*lo[1] + np.sin(t)*mo[1]) - Z_l*no[1]

# Velocity field in the upper surface
Vkep_u = (G*M/((R*au2cm)**2+(Z_u*au2cm)**2)**(3/2))**0.5 * R*au2cm /km2cm
Vz_u = - drot*Vkep_u*(-np.sin(t)*lo[2] + np.cos(t)*mo[2]) + Vsys
dVzu = linewidth(R, Z_u, source['Lw0'], source['p'], source['q'])
Vzup = Vz_u+dVzu; Vzum = Vz_u-dVzu; Vzur = np.dstack((Vzum,Vzup))

# Velocity field in the lower surface
Vkep_l = (G*M/((R*au2cm)**2+(Z_l*au2cm)**2)**(3/2))**0.5 * R*au2cm /km2cm
Vz_l = - drot*Vkep_l*(-np.sin(t)*lo[2] + np.cos(t)*mo[2]) + Vsys
dVzl = linewidth(R, Z_l, source['Lw0'], source['p'], source['q'])
Vzlp = Vz_l+dVzl; Vzlm = Vz_l-dVzl; Vzlr = np.dstack((Vzlm,Vzlp))

# Make masks
u_masks, l_masks = [],[]
for chan in vel_list:
    Vzu_mask = ((Vzur[:,:,0] <= chan-cw/2) * (Vzur[:,:,1] >= chan-cw/2)) + ((Vzur[:,:,0] <= chan+cw/2) * (Vzur[:,:,1] >= chan+cw/2))
    Vzl_mask = ((Vzlr[:,:,0] <= chan-cw/2) * (Vzlr[:,:,1] >= chan-cw/2)) + ((Vzlr[:,:,0] <= chan+cw/2) * (Vzlr[:,:,1] >= chan+cw/2))     
    Su_binary, _, _ = np.histogram2d(Sux[Vzu_mask].flatten(), Suy[Vzu_mask].flatten(), bins=[grid_dec*dpc, -grid_ra*dpc]); Su_binary = np.flip(Su_binary > 0, axis=1)
    Sl_binary, _, _ = np.histogram2d(Slx[Vzl_mask].flatten(), Sly[Vzl_mask].flatten(), bins=[grid_dec*dpc, -grid_ra*dpc]); Sl_binary = np.flip(Sl_binary > 0, axis=1)
    u_masks.append(Su_binary)
    l_masks.append(Sl_binary)

# Beam convolution
beam_pix = cf*int(beam/pix) # beam in pixels
kernel = circular_kernel(beam_pix) # circular kernel
u_masks_conv = dilate_masks(u_masks, kernel)
l_masks_conv = dilate_masks(l_masks, kernel)
all_masks = (np.array(u_masks_conv) + np.array(l_masks_conv)) > 0
print('Done.')

# Save fits or npy
if savefits == True:
    print('Saving fits...', end='', flush=True)
    if header['NAXIS'] == 4: hdu[0].data[0] = all_masks.astype(np.uint8)
    elif header['NAXIS'] == 3: hdu[0].data = all_masks.astype(np.uint8)
    hdu[0].header['BUNIT'] = 'bool'
    hdu[0].header['BMAJ'] = cf*beam
    hdu[0].header['BMIN'] = cf*beam
    hdu[0].header['BPA'] = 0
    hdu.writeto(pd+savefitsname, overwrite=True)
    print('Done.')
    print(pd+savefitsname+' was saved.')
else:
    print('Saving npy...', end='', flush=True)
    savename_u = source['name']+"_keplerianmask_upper"
    savename_l = source['name']+"_keplerianmask_lower"
    np.save(savename_u, u_masks_conv)
    np.save(savename_l, l_masks_conv)
    print('Done.')
    print(savename_u+'.npy and '+savename_l+'.npy were saved.')

# Make animation (if make_animation == True)
if make_animation == True:
    print('Making animation...', end='', flush=True)
    
    # Make upper surface contours
    R_list_r = np.linspace(0,Rmax,6)[1:]
    t_list_r = np.linspace(0,2*np.pi,2000)
    R, t = np.meshgrid(R_list_r, t_list_r) 
    Z_u = z_surf(R, source['z0_u'], source['p_u'], source['Rb_u'], source['q_u'])
    Sux_r = R*(np.cos(t)*lo[0] + np.sin(t)*mo[0]) + Z_u*no[0]
    Suy_r = R*(np.cos(t)*lo[1] + np.sin(t)*mo[1]) + Z_u*no[1]

    R_list_t = np.linspace(0,Rmax,2000)[1:]
    t_list_t = np.arange(0,2*np.pi,np.pi/4)
    R, t = np.meshgrid(R_list_t, t_list_t) 
    Z_u = z_surf(R, source['z0_u'], source['p_u'], source['Rb_u'], source['q_u'])
    Sux_t = R*(np.cos(t)*lo[0] + np.sin(t)*mo[0]) + Z_u*no[0]
    Suy_t = R*(np.cos(t)*lo[1] + np.sin(t)*mo[1]) + Z_u*no[1]

    # Make figure
    fig, ax = plt.subplots(1,2, figsize=(8,4), constrained_layout=True)
    extent = [np.max(dec)*dpc, np.min(dec)*dpc, np.min(ra)*dpc, np.max(ra)*dpc]

    def update(i):
        chan = chan_bottom + i
        ax[0].clear(); ax[1].clear()
        ax[0].imshow(data[chan], origin='lower', cmap='inferno', extent=extent)
        ax[1].imshow(data[chan], origin='lower', cmap='inferno', extent=extent)
        ax[1].contour(u_masks_conv[chan], levels=[0.5], colors=['w'], extent=extent)
        ax[1].contour(l_masks_conv[chan] - (u_masks_conv[chan]*l_masks_conv[chan]) , levels=[0.5], colors=['w'], alpha=[0.5], extent=extent)
        ax[0].set_title('Vlsr='+str(round(vel_list[chan],2))+' km/s (Vsys='+str(round(Vsys,2))+' km/s)')
        ax[1].set_title(str(cf)+'beam conv.')
        
        for i,r in enumerate(R_list_r):
            ax[0].plot(Suy_r[:,i], Sux_r[:,i], c='w', alpha=0.4)
        for i,t in enumerate(t_list_t):
            ax[0].plot(Suy_t[i], Sux_t[i], c='w', alpha=0.4)
        
        for j in [0,1]:
            ax[j].set_xlabel(r'$\Delta$RA [au]')
            ax[j].set_ylabel(r'$\Delta$DEC [au]')

    ani = FuncAnimation(fig, update, frames=chan_top-chan_bottom+1, interval=10)
    writer = HTMLWriter(fps=15)#, embed_frames=True)
    savehtml = source['name']+"_kepler_animation_test.html"
    ani.save(savehtml, writer=writer)
    print('Done.')
    print(savehtml+ ' was saved.')
