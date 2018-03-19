from PIL import Image as img
from PIL import ImageOps as opts
import numpy as np


pic=img.open('lionhead2.JPG')
pic2 = pic.resize((100,100))
w,h=pic2.size
pic2=opts.posterize(pic2,3)
pix=pic2.getcolors(w*h)
#pixels.sort(reverse=True)
#print(pix)
ColArr=[]
for i in range(len(pix)):
    RGBint=(pix[i][1][0]<<16) + (pix[i][1][1]<<8) + pix[i][1][2]
    #print(pix[i][1], ' - ', hex(pix[i][1][0]), hex(pix[i][1][1]), hex(pix[i][1][2]), hex(RGBint))
    #r,g,b=pixels[0][1]
    #print(pix[i][0],RGBint)
    ColArr.append([pix[i][0],RGBint])
ColArr.sort(reverse=True)
V1=int(len(ColArr)*0.1)
V2=int(len(ColArr)*0.5)
pic=opts.expand(pic,border=30,fill=ColArr[V1][1])
pic=opts.expand(pic,border=30,fill=ColArr[V2][1])
pic.show()
#npCol=np.asarray(ColArr)
print(len(ColArr))

