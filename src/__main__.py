from aura import AuraUsb
from screen import Screen

import time

import numpy as np
import matplotlib as mpl

from settings import ScreenSettings,MiscSettings

if MiscSettings.debug:
    from rich.console import Console
    console = Console()
    console.log("finding devices")

aura = AuraUsb()

if MiscSettings.debug:
    console.log(f"found devices: {aura.devices}")

screen = Screen(fps=ScreenSettings.fps,region=ScreenSettings.region or None)

def colormix(c1,c2,mix=0):
    c1=np.array(tuple(map(lambda x: x/255,c1)))
    c2=np.array(tuple(map(lambda x: x/255,c2)))
    return mpl.colors.to_rgb((1-mix)*c1 + mix*c2)

prev_color = MiscSettings.default_color

while True:
    now = time.time()
    colors = screen.get_colors()

    if MiscSettings.debug:
        console.print(f"██",style=f"rgb({colors[0][0]},{colors[0][1]},{colors[0][2]})",end="  ")
        console.print(f"██",style=f"rgb({colors[1][0]},{colors[1][1]},{colors[1][2]})")
        console.print(f"  ██  ",style=f"rgb({colors[4][0]},{colors[4][1]},{colors[4][2]})")
        console.print(f"██",style=f"rgb({colors[2][0]},{colors[2][1]},{colors[2][2]})",end="  ")
        console.print(f"██",style=f"rgb({colors[3][0]},{colors[3][1]},{colors[3][2]})")
        console.log(f"took {round((time.time()-now)*1000)}ms to get colors")

    color = colormix(prev_color,colors[4],0.3)   
    color = list(map(lambda x: round(x*255) ,color))
    aura.set_color(*color) 
    prev_color = color