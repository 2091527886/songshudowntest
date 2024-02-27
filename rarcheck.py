import pwd
from time import sleep
from unrar import rarfile
import os 
import _thread
import logging
from multiprocessing import Pool
src = "/home/16t/download/14001-27938/"
password = "www.songshudang.com"
compressed = 0
file_size = 0
files=os.listdir("/home/16t/download/14001-27938/")

#print(files)

for i in files:
    temp1=(src+i)
    print(i)
    rar = rarfile.RarFile(temp1,"r",pwd=password)
    rarnamelist = rar.infolist()
    for i in rarnamelist:
        compressed += i.compress_size
        file_size += i.file_size



print(compressed)
print(file_size)
print(compressed/file_size)
