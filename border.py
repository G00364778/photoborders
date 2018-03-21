"""
Python photo border utility
"""
from PIL import Image as img
from PIL import ImageOps as opts
from os import makedirs as mkd
import os
#import numpy as np
import ctypes
import json
from random import randint

posterizeval = 2 #default: 3
coloursort = False # True or False - sort by frequency
border = 'thick' # thick or thin or medium
sampledir = 'thm' # a folder to store thumbnail images in 
tnsize=(250,250) # thumbnail size
coloridx=(2,5) # selectable colour index, overwroittem if rand enabled
fileinfo=[] # place to store file info
initbool=False # check if inot was completed previously
rand=True #enable/disable random borders
#ColArr=[] # a new value to store the converted rgb values
#tn=0
# https://www.reddit.com/r/Python/comments/oixmu/add_entry_to_windows_7_context_menu_that_runs/

#def Mbox(title, text, style):
#    return ctypes.windll.user32.MessageBoxW(0, text, title, 0x40)

def bordersizes(img):
    w,h=img.size
    border1=int(w*0.05)
    border2=int(w*0.1)
    if border.lower().strip() == 'medium' or border.lower().strip() == 'med':
        border1//=2
        border2//=2
    elif border.lower().strip() == 'thin':
        border1//=3
        border2//=3
    return border1, border2

def filepathparse(filepathstr):
    global fileinfo
    filedir = os.path.dirname(filepathstr)
    filename, fileext = os.path.splitext((os.path.basename(filepathstr)))
    fileinfo=[filedir,filename,fileext]
    
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
    global coloridx, initbool
    initbool=True
    ColArr=[]
    #pic=img.open(r'C:\Users\Jattie\Pictures\lionhead2.JPG')
    filepathparse(jpegfilepath)
    pic=img.open(jpegfilepath)
    tn=img.open(jpegfilepath) # copy the pic th thumbnail
    tn.thumbnail(tnsize) # reduce thumbnail to tnsize
    #pic2 = pic.resize((100,100))
    border1,border2=bordersizes(tn)
    tnp=opts.posterize(tn,posterizeval)
    pix=tnp.getcolors()
    print('colours: ',len(pix))
    if rand==True:
        coloridx=(randint(0,len(pix)-1),randint(0,len(pix)-1))
    #ColArr=[] # a new value to store the converted rgb values
    print(coloridx)
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
    if len(fileinfo[0])>0:
        sampledir=r'{}\{}'.format(fileinfo[0],'thm')
    if initbool==False:
        return -1
    else:
        for i in range(len(colorArr)):
            for j in range(len(colorArr)):
                pic2 = thumbnail
                pic2=opts.expand(pic2,border=border1,fill=colorArr[j][1])
                pic2=opts.expand(pic2,border=border2,fill=colorArr[i][1])
                filename='thumb_{:02d}_{:02d}.jpg'.format(i,j)
                mkd(os.path.dirname('%s\\%s' % (sampledir,filename)), exist_ok=True)
                filepath=r'{}\{}'.format(sampledir,filename)
                pic2.save(filepath)
        pic2.close()
        thumbnail.close()

def make(pic, border1, border2, colorArr,coloridx):
    """
    Create a picture with borders using the info collected
    """
    if initbool==False:
        return -1
    else:
        border1,border2=bordersizes(pic)
        pic2=opts.expand(pic,border=border1,fill=colorArr[coloridx[1]][1])
        pic2=opts.expand(pic2,border=border2,fill=colorArr[coloridx[0]][1])
        filename='{}_border{}'.format(fileinfo[1],fileinfo[2].lower())
        if len(fileinfo[0])==0: #no path, only file info
            filepath=filename
        else:
            filepath=r'{}\{}'.format(fileinfo[0],filename)
        pic2.save(filepath)
        pic.close()
        pic2.close()



tn, pic, border1, border2, ColArr = init(r'C:\Users\Jattie\Documents\photoborders\lionhead2.JPG')
#maketh(tn, border1, border2, ColArr)
make(pic, border1, border2, ColArr, coloridx)
