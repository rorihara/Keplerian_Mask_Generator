import numpy as np
import astropy.units as U
from astropy.io import fits as FITS
from .functions import *

class LoadFits:
    def __init__(self, config, source):
        globals().update(config)
        globals().update(source)
       
        print('Source: '+name)
        self.load_data()
        if slice_image:
            self.imageslicer()
        self.pix2grid()

    def load_data(self):
        fitsfile = pd + fits
        with FITS.open(fitsfile) as hdu:
            header = hdu[0].header
            self.restfreq = header['RESTFRQ'] # Rest frequency
            fitslist = {0:'[RA,DEC,FREQ,STOKES]', 1:'[RA,DEC,STOKES,FREQ]', 2:'[RA,DEC,FREQ]'}
            if header['NAXIS'] == 4:
                if header['CTYPE3'] == 'FREQ':
                    self.fitstype = 0
                    for dic in ['CRVAL', 'CDELT', 'CTYPE', 'NAXIS', 'CRPIX', 'CUNIT']:
                        header[dic+'3'], header[dic+'4'] = header[dic+'4'], header[dic+'3']
                    self.data = hdu[0].data[0]
                else:
                    self.fitstype = 1
                    self.data = hdu[0].data[:,0]
                f_ref = header['CRVAL4'] # frequency of the reference channel
                f_ref_ind = header['CRPIX4'] # index of the reference channel
                self.df = header['CDELT4'] # channel width
                f_start = f_ref + (1-f_ref_ind)*self.df # frequency of the start channel
                nf = header['NAXIS4'] # number of channels
                self.cw = np.abs(header['CDELT4']*clight/self.restfreq)/km2cm # Channel width in km/s
            elif header['NAXIS'] == 3:
                self.fitstype = 2
                self.data = hdu[0].data
                f_ref = header['CRVAL3'] # frequency of the reference channel
                f_ref_ind = header['CRPIX3'] # index of the reference channel
                self.df = header['CDELT3'] # channel width
                f_start = f_ref + (1-f_ref_ind)*self.df # frequency of the start channel
                nf = header['NAXIS3'] # number of channels
                self.cw = np.abs(header['CDELT3']*clight/self.restfreq)/km2cm # Channel width in km/s
            self.pix = header['CDELT2'] * deg2arcsec # Pixel size
            imsize = header['NAXIS1'] # Image size
            if 'CASAMBM' in header:
                self.beam = hdu[1].data[0][0]
                if hdu[1].header['TUNIT1'] == 'deg': self.beam *= deg2arcsec
            else: self.beam = header['BMAJ'] * deg2arcsec
            imc = int(imsize / 2) # Image center
            indlist = np.arange(0, imsize)
            self.header = header
            self.ra = -(indlist - imc) * self.pix
            self.dec = (indlist - imc) * self.pix
            
            f_list = np.linspace(f_start, f_start+self.df*(nf-1), nf)
            self.vel_list = clight*(self.restfreq-f_list)/self.restfreq/km2cm
            self.vel_list_vsys = self.vel_list - Vsys
            
            print('FITS Type: '+str(self.fitstype)+' ' +fitslist[self.fitstype])

    def imageslicer(self):
        slice_arcsec = int(round(Rout / dpc)) + 1
        ras = np.argmin((self.ra - slice_arcsec) ** 2)
        rae = np.argmin((self.ra + slice_arcsec) ** 2) + 1
        decs = np.argmin((self.dec + slice_arcsec) ** 2)
        dece = np.argmin((self.dec - slice_arcsec) ** 2) + 1
        self.ra = self.ra[ras:rae]
        self.dec = self.dec[decs:dece]
        self.data = self.data[:, decs:dece, ras:rae]

    def pix2grid(self):
        print('slice_image: '+str(slice_image))
        print('Data shape: '+str(self.data.shape))
        self.grid_ra = np.append(self.ra + self.pix/2, np.min(self.ra - self.pix/2))
        self.grid_dec = np.append(self.dec - self.pix/2, np.max(self.dec + self.pix/2))
