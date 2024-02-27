import pwd
from time import sleep

import os 
import _thread
import logging
import multiprocessing 
overwrite = True

src = "/home/md1/downloadtemp/"
password = "www.songshudang.com"
#src = "/home/md1/1/"
compressed = 0
file_size = 0
#files=os.listdir("/home/16t/download/14001-27938/")
rarlist = []
for root, dirs, files in os.walk(src, topdown=False):
    for name in files:
        if os.path.splitext(name)[1] ==".rar" and "}" in os.path.splitext(name)[0]:
            rarlist.append(os.path.join(root, name))
        
        
        
    for name in dirs:
        #print(os.path.join(root, name))
        a = 1
for i in rarlist:
    print(i)