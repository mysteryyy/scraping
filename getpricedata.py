import os
import pickle as pck
import sys
from loading_data import ext

class extract:

    def __init__(self):
       pass
       os.system('docker build . -t scrape')
    
    def enter_data(self,symbol,date1,date2):
       os.system('docker volume create data4')
       os.system('docker run -e SYMBOL={}  -e DATE1={}  -e DATE2={} -v data4:/usr/share/app scrape'.format(symbol,date1,date2))
       dir_loc = '/var/lib/docker/volumes/data4/_data'
       k = ext().give_file(dir_loc,'daily_data')
       os.system('docker volume prune -f')
       os.chdir('/root/dock1/dock')
       return k

    
    def enter_fin_data(self,symbol,date1='-',date2='-'):
       os.system('docker volume create data4')
       os.system('docker run -e SYMBOL={}  -e DATE1={}  -e DATE2={} -v data4:/usr/share/app scrape'.format(symbol,date1,date2))
       dir_loc = '/var/lib/docker/volumes/data4/_data'
       k = ext().give_file(dir_loc,'finalkfr1')
       os.system('docker volume prune -f')
       os.chdir('/root/dock1/dock')
       return k

    def del_cont(self): 
        os.system('docker container prune -f')
