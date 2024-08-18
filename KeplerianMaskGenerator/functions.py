import numpy as np
import cv2
import astropy.constants as C
import astropy.units as U

# Constants and units
G = C.G.cgs.value # Gravitational constant in cgs units (cm^3 g^-1 s^-2)
clight = C.c.cgs.value # Speed of light in cgs units (cm s^-1)
deg2arcsec = (U.deg).to(U.arcsec)  # deg to arcsec
au2cm = (U.au).to(U.cm) # au to cm
km2cm = (U.km).to(U.cm) # km to cm
Ms2g =  (U.M_sun).to(U.g) # Msun to g

# Rotation matrix
def rot(i, p): 
    i, p = np.radians(i), np.radians(p)
    ci, si = np.cos(i), np.sin(i)
    cp, sp = np.cos(p), np.sin(p)
    return np.array([[cp, -sp * ci, -sp * si], [sp, cp * ci, cp * si], [0, -si, ci]])

# Surface of the disk
def h_surf(r, h0, p, Rb, q, R=100):
    return h0*(r/R)**p * np.exp(-(r/Rb)**q)

# Linewidth
def linewidth(r, h, L0, p, q):
    return L0 * (r/100)**p * (h/100)**q

# Circulate kernel for beam convolution
def circular_kernel(beam_pix):
    L = np.arange(-round(beam_pix/2), round(beam_pix/2) + 1)
    X, Y = np.meshgrid(L, L)
    kernel = (X**2 + Y**2) <= round(beam_pix/2)**2
    return kernel.astype(np.uint8)

# Dilate masks to make them thicker
def dilate_masks(masks, kernel):
    return [cv2.dilate(mask.astype(np.uint8), kernel, iterations=1) for mask in masks]
