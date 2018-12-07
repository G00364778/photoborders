import ctypes
import sys
import border as b
import os
#import subprocess as sub
#from time import sleep

try:
    sys.argv[1:]
except NameError:
    argc=0
else:
    argc=len(sys.argv)
if argc<=1:
    ctypes.windll.user32.MessageBoxW(0, 'Error, a filename is required!' ,'Error', 0x30)
    exit(-1)
elif argc==2: # a single parameter
    filepath=sys.argv[1]

cdir=os.path.dirname(filepath)
b.sampledir=cdir+r'\thm'

#https://stackoverflow.com/questions/34840838/how-to-specify-what-actually-happens-when-yes-no-is-clicked-with-ctypes-messageb

#ctypes.windll.user32.MessageBoxW(0, 'Filename: {}'.format(filepath),'Python Photo Frame Script', 0x40)

b.posterizeval=3
tn, pic, border1, border2, ColArr = b.init(sys.argv[1])
#b.maketh(tn, border1, border2, ColArr)
b.make(pic, border1, border2, ColArr, b.coloridx)
#sleep(5)
#sub.Popen(r'explorer /select, "{}\"'.format(b.sampledir))
