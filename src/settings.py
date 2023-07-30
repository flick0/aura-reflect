class MiscSettings:
    default_color:list = [0x00,0x00,0x00]
    debug:bool = False
    color_fade_step:float = 0.3
    tps: int = 20
    starting_angle:int = 0
    angle_step = 5
    tertiary_color_mix = 0.7

class ImageSettings:
    color:float = 2.7
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
    fps:int = 20
    region:tuple[int,int,int,int] = None

