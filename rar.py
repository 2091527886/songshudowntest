import pwd
from time import sleep
from unrar import rarfile
import os 
import _thread
import logging
import multiprocessing 
overwrite = True
def testrar(a,rarname):
    rar = rarfile.RarFile(rarname,"r",pwd=password)
    #rarnamelist = rar.infolist()
    rartest = rar.testrar()
    #print(type(rartest))
    print(a)
    if rartest !=None:
        print(a,rartest)
def extrarar(rarname):
    #rar = rarfile.RarFile(rarname,"r",pwd=password)
    try:
        #file_names = rar.getnames()
        #print(rar.namelist())
        #print(rar.filename)
        rar = rarfile.RarFile(rarname,"r",pwd=password)
        '''
        for file_name in file_names:
            # 构建完整的文件路径
            file_path = os.path.join(src, file_name)
            # 如果文件存在，则删除它
            if os.path.exists(file_path):
                os.remove(file_path)
        '''
        rar.extractall(src)
        os.rename(rarname,rarname+".fin")
        print("win@",rarname)
        #rar.close()
    except:
        print("failed@",rarname)
        #rar.close()
    #print(i)
    #os.remove(rarname)
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
        print(os.path.join(root, name))
oaaa = []

    

p = multiprocessing.Pool(32)
for i in rarlist:
    a = p.map_async(extrarar,(i,))
    oaaa.append(a)
for adc in oaaa:
    adc.get(99999)
    
    
p.close()
p.join()
