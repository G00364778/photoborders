from PIL import Image as img
from PIL import ImageOps as opts
from os import makedirs as mkd
from os import path as osp
#import numpy as np
import ctypes
import json

# 
posterizeval = 1 #default: 3
coloursort = False # True or False - sort by frequency
border = 'thick' # thick or thin or medium
sampledir = 'thm'
tnsize=(250,250)

# https://www.reddit.com/r/Python/comments/oixmu/add_entry_to_windows_7_context_menu_that_runs/
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

#pic=img.open(r'C:\Users\Jattie\Pictures\lionhead2.JPG')
pic=img.open(r'lionhead2.JPG')
tn=pic # copy the pic th thumbnail
tn.thumbnail(tnsize) # reduce thumbnail to tnsize
#pic2 = pic.resize((100,100))
w,h=tn.size
border1=int(w*0.05)
border2=int(w*0.1)
if border.lower().strip() == 'medium' or border.lower().strip() == 'med':
    border1//=2
    border2//=2
elif border.lower().strip() == 'thin':
    border1//=3
    border2//=3


tnp=opts.posterize(tn,posterizeval)
pix=tnp.getcolors()
print('colours: ',len(pix))
ColArr=[] # a new value to store the converted rgb values
for i in range(len(pix)): # loop through all the colours
    RGBint=(pix[i][1][0]<<16) + (pix[i][1][1]<<8) + pix[i][1][2] # convert tuple to rgb
    ColArr.append([pix[i][0],RGBint]) # append conversions
if coloursort == True: # sort if selected
    ColArr.sort(reverse=True)
# save the color array for reuse 
mkd(osp.dirname('%s\\%s' % ('tmp','tmp.txt')), exist_ok=True)
with open(r'tmp\pix.json', 'w') as outfile: json.dump(pix, outfile)
#with open(r'tmp\pix.json', 'r') as json_file: pix = json.load(json_file) # read data

#loop throug all the colours and create samples
for i in range(len(ColArr)):
    for j in range(len(ColArr)):
        pic2 = tn
        pic2=opts.expand(pic2,border=border1,fill=ColArr[j][1])
        pic2=opts.expand(pic2,border=border2,fill=ColArr[i][1])
        filename='thumb_{:02d}_{:02d}.jpg'.format(i,j)
        mkd(osp.dirname('%s\\%s' % (sampledir,filename)), exist_ok=True)
        filepath=r'{}\{}'.format(sampledir,filename)
        pic2.save(filepath)
#inf=Mbox('Input', 'Save to file?', 4)
#if inf==6: # Yes
#    pic.save('border.jpg')
#else: # No
#    pic.show()


