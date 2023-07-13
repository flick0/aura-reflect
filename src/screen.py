import dxcam
import numpy as np
from PIL import Image, ImageEnhance

from settings import ImageSettings

def avg_color(*colors:list[tuple[int,int,int]])->tuple[int,int,int]:
    colors = np.array(colors)
    return tuple(np.average(colors,axis=0).astype(int))
    
class Screen:
    camera = dxcam.create()
    
    def __init__(self,*,fps:int=0,region:tuple[int,int,int,int]=None):
        self.region = region
        self.camera.start(region=region,target_fps=fps,video_mode=True)

    def get_frame(self):
        img = Image.fromarray(self.camera.get_latest_frame())
        return img
    
    def get_colors(self)->tuple[tuple[int,int,int]]:
        img = self.get_frame()
        img = img.resize((4,4),ImageSettings.resample)

        if ImageSettings.brightness:
            img = ImageEnhance.Brightness(img).enhance(ImageSettings.brightness)
        if ImageSettings.contrast:
            img = ImageEnhance.Contrast(img).enhance(ImageSettings.contrast)
        if ImageSettings.color:
            img = ImageEnhance.Color(img).enhance(ImageSettings.color)
        if ImageSettings.sharpness:
            img = ImageEnhance.Sharpness(img).enhance(ImageSettings.sharpness)

        return (
            avg_color(img.getpixel((0,0)),img.getpixel((1,0)),img.getpixel((0,1)),img.getpixel((1,1))), # top_left
            avg_color(img.getpixel((2,0)),img.getpixel((3,0)),img.getpixel((2,1)),img.getpixel((3,1))), # top_right
            avg_color(img.getpixel((0,2)),img.getpixel((1,2)),img.getpixel((0,3)),img.getpixel((1,3))), # bottom_left
            avg_color(img.getpixel((2,2)),img.getpixel((3,2)),img.getpixel((2,3)),img.getpixel((3,3))), # bottom_right
            avg_color(img.getpixel((1,1)),img.getpixel((2,1)),img.getpixel((1,2)),img.getpixel((2,2))), # center
        )

        

        


    
    
