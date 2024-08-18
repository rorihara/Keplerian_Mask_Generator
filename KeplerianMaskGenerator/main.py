from .load_fits import LoadFits
from .make_mask import MakeMask
from .saver import MaskSaver

class generator:
    def __init__(self, config, source):
        self.config = config
        self.source = source

    def generate_mask(self, slice_image):
        self.slice_image = slice_image
        self.__loadfits = LoadFits(self.config, self.source, self.slice_image)
        self.__makemask = MakeMask(self.config, self.source, self.__loadfits)
        self.data = self.__loadfits.data
        self.all_mask = self.__makemask.all_masks
        self.upper_mask = self.__makemask.u_masks_conv
        self.lower_mask = self.__makemask.l_masks_conv
        self.ra = self.__loadfits.ra
        self.dec = self.__loadfits.dec
        self.vel = self.__loadfits.vel_list

    def save_mask(self, save_fits, save_npy, save_animation, vrange=3):
        masksaver = MaskSaver(self.config, self.source, self.__makemask)
        if save_fits:
            if self.slice_image:
                print("The FITS file will not be saved because the image has been sliced.")
            else:
                masksaver.save_fits()
        if save_animation:
            masksaver.save_animation(vrange)
        if save_npy:
            masksaver.save_npy()
