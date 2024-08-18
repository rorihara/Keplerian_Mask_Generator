from .load_fits import LoadFits
from .make_mask import MakeMask
from .saver import MaskSaver

class generator:
    def __init__(self, config, source):
        self.config = config
        self.source = source

    def generate_mask(self, slice_image):
        self.slice_image = slice_image
        self.loadfits = LoadFits(self.config, self.source, self.slice_image)
        self.makemask = MakeMask(self.config, self.source, self.loadfits)
        return self.loadfits.data, self.makemask.all_masks, self.makemask.u_masks_conv, self.makemask.l_masks_conv

    def save_mask(self, save_fits, save_npy, save_animation, vrange=3):
        masksaver = MaskSaver(self.config, self.source, self.makemask)
        if save_fits:
            if self.slice_image:
                print("The FITS file will not be saved because the image has been sliced.")
            else:
                masksaver.save_fits()
        if save_animation:
            masksaver.save_animation(vrange)
        if save_npy:
            masksaver.save_npy()
