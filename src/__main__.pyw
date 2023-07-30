from aura import AuraUsb
from screen import Screen

import signal 
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
    return list(map(lambda x: round(x*255) ,mpl.colors.to_rgb((1-mix)*c1 + mix*c2))) 


def angle_color(angle, center, c1,c2,c3,c4):

    if angle < 90:
        tert = colormix(c1,c2,angle/90)
    elif angle < 180:
        tert = colormix(c2,c3,(angle-90)/90)
    elif angle < 270:
        tert = colormix(c3,c4,(angle-180)/90)
    else:
        tert = colormix(c4,c1,(angle-270)/90)
        
    return colormix(center,tert,MiscSettings.tertiary_color_mix)


prev_color = MiscSettings.default_color

class Exiter():
    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.change_state)

    def change_state(self, signum, frame):
        print("exiting")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def exit(self):
        return self.state

exiter = Exiter()

print("ctrl + c to exit ")

angle = MiscSettings.starting_angle

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

    color = colormix(prev_color,angle_color(angle,colors[4],colors[0],colors[1],colors[2],colors[3]),MiscSettings.color_fade_step)   
    # color = list(map(lambda x: round(x*255) ,color))
    aura.set_color(*color)
    prev_color = color

    angle += MiscSettings.angle_step
    angle %= 360

    tps = MiscSettings.tps
    elapsed = time.time()-now

    if elapsed < 1/tps:
        time.sleep(1/tps-elapsed)

    if exiter.exit():
        aura.close()
        print("closed all aura devices")
        break