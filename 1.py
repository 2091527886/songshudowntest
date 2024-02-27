import os 
floderdir = "/home/16t/download/14001-27938"
floder22 = os.listdir(floderdir)
unrar1 = []
for i in floder22:

    if not i.endswith(".rar"):
        unrar1.append(i)
print(unrar1)
