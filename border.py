from PIL import Image as img
from PIL import ImageOps as opts
import numpy as np
import ctypes


# https://www.reddit.com/r/Python/comments/oixmu/add_entry_to_windows_7_context_menu_that_runs/
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

pic=img.open(r'C:\Users\Jattie\Pictures\lionhead2.JPG')
pic2 = pic.resize((100,100))
w,h=pic2.size
pic2=opts.posterize(pic2,3)
pix=pic2.getcolors(w*h)
ColArr=[]
for i in range(len(pix)):
    RGBint=(pix[i][1][0]<<16) + (pix[i][1][1]<<8) + pix[i][1][2]
    ColArr.append([pix[i][0],RGBint])
ColArr.sort(reverse=True)
V1=int(len(ColArr)*0.5)
V2=int(len(ColArr)*0.1)
pic=opts.expand(pic,border=30,fill=ColArr[V1][1])
pic=opts.expand(pic,border=30,fill=ColArr[V2][1])
inf=Mbox('Input', 'Save to file?', 4)
if inf==6: # Yes
    pic.save('border.jpg')
else: # No
    pic.show()


