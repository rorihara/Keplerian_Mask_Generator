import os
import shutil
import matplotlib.pyplot as plt
from .functions import *
import astropy.io.fits as FITS
from matplotlib.animation import FuncAnimation
from matplotlib.animation import HTMLWriter

class MaskSaver:
    def __init__(self, config, source, makemask):
        globals().update(config)
        globals().update(source)
        self.makemask = makemask

    def __getattr__(self, name):
        return getattr(self.makemask, name)
        
    def save_fits(self):
        print('Saving fits...', end='', flush=True)
        savefitsname = fits.split('.fits')[0]+'_keplerianmask.fits'
        if os.path.isfile(savefitsname): os.remove(savefitsname)
        shutil.copy(pd+fits, savefitsname)
        
        with FITS.open(savefitsname) as hduw:
            if self.fitstype == 0:
                hduw[0].data = self.all_masks.astype(np.float32)[:,np.newaxis]
                for dic in ['CRVAL', 'CDELT', 'CTYPE', 'NAXIS', 'CRPIX', 'CUNIT']:
                    hduw[0].header[dic+'3'], hduw[0].header[dic+'4'] = self.header[dic+'3'], self.header[dic+'4']
            elif self.fitstype == 1:
                hduw[0].data = self.all_masks.astype(np.float32)[:,np.newaxis]
            elif self.fitstype == 2:
                hduw[0].data = self.all_masks.astype(np.float32)
            hduw[0].header['BUNIT'] = ''
            hduw[0].header['BMAJ'] = cf*self.beam / deg2arcsec
            hduw[0].header['BMIN'] = cf*self.beam / deg2arcsec
            hduw[0].header['BPA'] = 0
            del hduw[0].header['HISTORY']
            if 'CASAMBM' in self.header: del hduw[0].header['CASAMBM']
            hduw[0].writeto(savefitsname, overwrite=True)
        print('Done.')
        print(savefitsname+' was saved.')

    def save_npy(self):
        print('Saving npy...', end='', flush=True)
        savename_u = fits.split('.fits')[0]+"_keplerianmask_upper"
        savename_l = fits.split('.fits')[0]+"_keplerianmask_lower"
        np.save(savename_u, self.u_masks_conv)
        np.save(savename_l, self.l_masks_conv)
        print('Done.')
        print(savename_u+'.npy and '+savename_l+'.npy were saved.')

    def save_animation(self, vrange):
        lo, mo, no = self.basis_o
        print('Making animation...', end='', flush=True)
        # Make upper surface contours
        R_list_r = np.linspace(0,Rout,6)[1:]
        t_list_r = np.linspace(0,2*np.pi,2000)
        R, t = np.meshgrid(R_list_r, t_list_r) 
        H_u = h_surf(R, h0_u, p_u, Rb_u, q_u)
        Sux_r = R*(np.cos(t)*lo[0] + np.sin(t)*mo[0]) + H_u*no[0] + dDEC
        Suy_r = R*(np.cos(t)*lo[1] + np.sin(t)*mo[1]) + H_u*no[1] + dRA

        R_list_t = np.linspace(0,Rout,2000)[1:]
        t_list_t = np.arange(0,2*np.pi,np.pi/4)
        R, t = np.meshgrid(R_list_t, t_list_t) 
        H_u = h_surf(R, h0_u, p_u, Rb_u, q_u)
        Sux_t = R*(np.cos(t)*lo[0] + np.sin(t)*mo[0]) + H_u*no[0] + dDEC
        Suy_t = R*(np.cos(t)*lo[1] + np.sin(t)*mo[1]) + H_u*no[1] + dRA

        if self.df > 0:
            chan_top = np.argmin(np.abs(self.vel_list_vsys + vrange))
            chan_bottom = np.argmin(np.abs(self.vel_list_vsys - vrange))
        else:
            chan_top = np.argmin(np.abs(self.vel_list_vsys - vrange))
            chan_bottom = np.argmin(np.abs(self.vel_list_vsys + vrange))

        # Make figure
        fig, ax = plt.subplots(1,2, figsize=(8,4), constrained_layout=True)
        extent = [np.max(self.dec)*dpc, np.min(self.dec)*dpc, np.min(self.ra)*dpc, np.max(self.ra)*dpc]

        def update(i):
            chan = chan_bottom + i
            ax[0].clear(); ax[1].clear()
            ax[0].imshow(self.data[chan], origin='lower', cmap='inferno', extent=extent)
            ax[1].imshow(self.data[chan], origin='lower', cmap='inferno', extent=extent)
            ax[1].contour(self.u_masks_conv[chan], levels=[0.5], colors=['w'], extent=extent)
            ax[1].contour(self.l_masks_conv[chan] - (self.u_masks_conv[chan]*self.l_masks_conv[chan]) , levels=[0.5], colors=['w'], alpha=[0.5], extent=extent)
            ax[0].set_title('Vlsr='+str(round(self.vel_list[chan],2))+' km/s (Vsys='+str(round(Vsys,2))+' km/s)')
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
        savehtml = fits.split('.fits')[0]+"_kepler_animation.html"
        ani.save(savehtml, writer=writer)
        print('Done.')
        print(savehtml+ ' was saved.')
