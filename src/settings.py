class MiscSettings:
    debug:bool = False

class AuraSettings:
    tps: int = 20
    
class ColorSettings:
    default_color:list = [0x00,0x00,0x00]
    color_fade_step:float = 0.3

    default_tertiary_angle:int = 0
    tertiary_angle_step:int = 5
    tertiary_color_mix:float = 0.7
    
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
