from PIL import Image as img
from PIL import ImageOps as opts
from os import makedirs as mkd
from os import path as osp
#import numpy as np
#import ctypes

# 
posterizeval = 2 #default: 3
coloursort = False # True or False - sort by frequency
border1 = 5
border2 = 15
sampledir = 'thm'

# https://www.reddit.com/r/Python/comments/oixmu/add_entry_to_windows_7_context_menu_that_runs/
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

#pic=img.open(r'C:\Users\Jattie\Pictures\lionhead2.JPG')
pic=img.open(r'lionhead2.JPG')
pic2 = pic.resize((100,100))
w,h=pic2.size
pic2=opts.posterize(pic2,posterizeval)
pix=pic2.getcolors()
print('colours: ',len(pix))
ColArr=[]
for i in range(len(pix)):
    RGBint=(pix[i][1][0]<<16) + (pix[i][1][1]<<8) + pix[i][1][2]
    ColArr.append([pix[i][0],RGBint])
if coloursort == True:
    ColArr.sort(reverse=True)

#V1=int(len(ColArr)*0.9)
#V2=int(len(ColArr)*0.01)
for i in range(len(ColArr)):
    for j in range(len(ColArr)):
        pic2 = pic.resize((100,100))
        pic2=opts.expand(pic2,border=border1,fill=ColArr[i][1])
        pic2=opts.expand(pic2,border=border2,fill=ColArr[j][1])
        filename='thumb_{:02d}_{:02d}.jpg'.format(i,j)
        mkd(osp.dirname('%s\\%s' % (sampledir,filename)), exist_ok=True)
        filepath=r'{}\{}'.format(sampledir,filename)
        pic2.save(filepath)
#inf=Mbox('Input', 'Save to file?', 4)
#if inf==6: # Yes
#    pic.save('border.jpg')
#else: # No
#    pic.show()


