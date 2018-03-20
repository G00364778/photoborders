"""
Python photo border utility
"""
from PIL import Image as img
from PIL import ImageOps as opts
from os import makedirs as mkd
from os import path as osp
#import numpy as np
import ctypes
import json

posterizeval = 1 #default: 3
coloursort = False # True or False - sort by frequency
border = 'thick' # thick or thin or medium
sampledir = 'thm'
tnsize=(250,250)

#ColArr=[] # a new value to store the converted rgb values
#tn=0
# https://www.reddit.com/r/Python/comments/oixmu/add_entry_to_windows_7_context_menu_that_runs/

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def init(jpegfilepath=r'lionhead2.JPG'):
    """
    Initialise the thumbnailer colour array and border width using the default variables
    return variables
        tn      - the thumbnail data object generate from the image passed in
        pic     - picture data object
        border1 - The boder one with calculated 
        border2 - The boder two with calculated 
        ColArr  - The colour array returned analysing the image
    """
    ColArr=[]
    #pic=img.open(r'C:\Users\Jattie\Pictures\lionhead2.JPG')
    pic=img.open(jpegfilepath)
    tn=img.open(jpegfilepath) # copy the pic th thumbnail
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
    #ColArr=[] # a new value to store the converted rgb values
    for i in range(len(pix)): # loop through all the colours
        RGBint=(pix[i][1][0]<<16) + (pix[i][1][1]<<8) + pix[i][1][2] # convert tuple to rgb
        ColArr.append([pix[i][0],RGBint]) # append conversions
    if coloursort == True: # sort if selected
        ColArr.sort(reverse=True)
    # save the color array for reuse 
    #mkd(osp.dirname('%s\\%s' % ('tmp','tmp.txt')), exist_ok=True)
    #with open(r'tmp\pix.json', 'w') as outfile: json.dump(pix, outfile)
    #with open(r'tmp\pix.json', 'r') as json_file: pix = json.load(json_file) # read data
    return tn, pic, border1, border2, ColArr

#loop throug all the colours and create samples

def maketh(thumbnail, border1, border2, colorArr):
    """
    Make Thumbnails by looping through all the colours twice for inner and outer borders and 
    generate samples in the thumbnail folder
    Pass values in returned by init

    thumbnail   -   thumabnail data object
    border1     -   border 1 value returned or int, tyoically 30
    border2     -   border 2 value returned or int, tyoically 30 
    colorArr    -   the colour array returned by init
    """
    for i in range(len(colorArr)):
        for j in range(len(colorArr)):
            pic2 = thumbnail
            pic2=opts.expand(pic2,border=border1,fill=colorArr[j][1])
            pic2=opts.expand(pic2,border=border2,fill=colorArr[i][1])
            filename='thumb_{:02d}_{:02d}.jpg'.format(i,j)
            mkd(osp.dirname('%s\\%s' % (sampledir,filename)), exist_ok=True)
            filepath=r'{}\{}'.format(sampledir,filename)
            pic2.save(filepath)
#inf=Mbox('Input', 'Save to file?', 4)
#if inf==6: # Yes
#    pic.save('border.jpg')
#else: # No
#    pic.show()

# tn, border1, border2, ColArr = th_init()
# th_make(tn, border1, border2, ColArr)
