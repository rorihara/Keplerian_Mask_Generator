import numpy as np
import cv2
from .functions import *

class MakeMask:
    def __init__(self, config, source, loadfits):
        globals().update(config)
        globals().update(source)
        self.loadfits = loadfits

        print('Making keplerian masks...', end='', flush=True)
        self.basis_vectors()
        self.surface_coords()
        self.velocity_fields()
        self.create_binary()
        self.convolved_masks()
        print('Done.')

    def __getattr__(self, name):
        return getattr(self.loadfits, name)

    def basis_vectors(self):
        no = rot(incl, pa)[:, 2] # normal vector of the disk midplane
        ez = rot(0, 0)[:, 2] # z-axis vector (line of sight)
        lo = np.cross(no, ez); lo /= np.linalg.norm(lo)
        mo = np.cross(no, lo)
        self.basis_o = (lo, mo, no) # basis vectors
    
    def surface_coords(self):
        lo, mo, no = self.basis_o
        R_list = np.arange(0, Rout+self.pix*dpc/2, self.pix*dpc/2)[1:]
        t_list = np.arange(0, 2*np.pi, self.pix*dpc/Rout/2)
        self.R, self.t = np.meshgrid(R_list, t_list) 
        self.H_u = h_surf(self.R, h0_u, p_u, Rb_u, q_u)
        if same_upperlower: H_l = H_u
        else: self.H_l = h_surf(self.R, h0_l, p_l, Rb_l, q_l)
        
        self.Sux = self.R*(np.cos(self.t)*lo[0] + np.sin(self.t)*mo[0]) + self.H_u*no[0] + dDEC
        self.Suy = self.R*(np.cos(self.t)*lo[1] + np.sin(self.t)*mo[1]) + self.H_u*no[1] + dRA
        self.Slx = self.R*(np.cos(self.t)*lo[0] + np.sin(self.t)*mo[0]) - self.H_l*no[0] + dDEC
        self.Sly = self.R*(np.cos(self.t)*lo[1] + np.sin(self.t)*mo[1]) - self.H_l*no[1] + dRA
    
    def velocity_fields(self):
        lo, mo, no = self.basis_o
    # Velocity field in the upper surface
        Vkep_u = (G*Ms*Ms2g/((self.R*au2cm)**2+(self.H_u*au2cm)**2)**(3/2))**0.5 * self.R*au2cm /km2cm
        Vz_u = - vel_sign*Vkep_u*(-np.sin(self.t)*lo[2] + np.cos(self.t)*mo[2]) + Vsys
        dVzu = linewidth(self.R, self.H_u, L0, p, q)
        Vzup = Vz_u+dVzu; Vzum = Vz_u-dVzu; self.Vzur = np.dstack((Vzum,Vzup))
    # Velocity field in the lower surface
        Vkep_l = (G*Ms*Ms2g/((self.R*au2cm)**2+(self.H_l*au2cm)**2)**(3/2))**0.5 * self.R*au2cm /km2cm
        Vz_l = - vel_sign*Vkep_l*(-np.sin(self.t)*lo[2] + np.cos(self.t)*mo[2]) + Vsys
        dVzl = linewidth(self.R, self.H_l, L0, p, q)
        Vzlp = Vz_l+dVzl; Vzlm = Vz_l-dVzl; self.Vzlr = np.dstack((Vzlm,Vzlp))

    def create_binary(self):
        self.u_masks, self.l_masks = [],[]
        for chan in self.vel_list:
            Vzu_mask = ((self.Vzur[:,:,0] <= chan-self.cw/2) * (self.Vzur[:,:,1] >= chan-self.cw/2)) + ((self.Vzur[:,:,0] <= chan+self.cw/2) * (self.Vzur[:,:,1] >= chan+self.cw/2))
            Vzl_mask = ((self.Vzlr[:,:,0] <= chan-self.cw/2) * (self.Vzlr[:,:,1] >= chan-self.cw/2)) + ((self.Vzlr[:,:,0] <= chan+self.cw/2) * (self.Vzlr[:,:,1] >= chan+self.cw/2))     
            Su_binary, _, _ = np.histogram2d(self.Sux[Vzu_mask].flatten(), self.Suy[Vzu_mask].flatten(), bins=[self.grid_dec*dpc, -self.grid_ra*dpc])
            Su_binary = np.flip(Su_binary > 0, axis=1)
            Sl_binary, _, _ = np.histogram2d(self.Slx[Vzl_mask].flatten(), self.Sly[Vzl_mask].flatten(), bins=[self.grid_dec*dpc, -self.grid_ra*dpc])
            Sl_binary = np.flip(Sl_binary > 0, axis=1)
            self.u_masks.append(Su_binary)
            self.l_masks.append(Sl_binary)
    
    def convolved_masks(self):
        beam_pix = cf*int(self.beam/self.pix) # beam in pixels
        kernel = circular_kernel(beam_pix) # circular kernel
        self.u_masks_conv = dilate_masks(self.u_masks, kernel) > 0
        self.l_masks_conv = dilate_masks(self.l_masks, kernel) > 0
        self.all_masks = (np.array(self.u_masks_conv) + np.array(self.l_masks_conv)) > 0
