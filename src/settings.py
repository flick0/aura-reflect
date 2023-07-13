class MiscSettings:
    default_color:list = [0x00,0x00,0x00]
    debug:bool = False
    color_fade_step:float = 0.3

class ImageSettings:
    color:float = 3.0
    contrast:float = None
    brightness:float = None
    sharpness:float = None

    resample = 5
    # NEAREST = 0
    # BOX = 4
    # BILINEAR = 2
    # HAMMING = 5
    # BICUBIC = 3
    # LANCZOS = 1

class ScreenSettings:
    fps:int = 30
    region:tuple[int,int,int,int] = None

