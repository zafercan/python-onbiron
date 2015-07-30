from __future__ import print_function
from collections import OrderedDict
import platform
from uuid import getnode as get_mac
import fcntl, socket, struct 
import glob
import re
import os
import time
import requests
import urllib2


class SystemInfo(object):
    
    ramInfo = None 
    interval = 0.1
    
    def __init__(self):
                
        self.ramInfo = OrderedDict()
        with open('/proc/meminfo') as f:
            for line in f:
                self.ramInfo[line.split(':')[0]] = line.split(':')[1].strip()
                  
    def getEthMac(self):
        
        ifname = 'eth0'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
        macEth =  ':'.join(['%02x' % ord(char) for char in info[18:24]])
        return macEth
    
    def getWlanMac(self):
        
        # get mac
        macWlan = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
        return macWlan
    
    def getRegId(self):
        
        regid = get_mac()
        return regid    
    
    def getOsVersion(self):
        
        version = platform.dist()[1]
        return version
    
    def getFWVersion(self):
        
        FWVersion = float(platform.dist()[1])
        return FWVersion
            
    def getTotalRam(self):
        
        ramInfo = self.ramInfo
        ramKB = float(format(ramInfo['MemTotal']).split(' ')[0])
        ramGB = ramKB/1024/1024
        ramGB = round(ramGB)
        return ramGB
    
    def getFreeRam(self):
         
        ramInfo = self.ramInfo
        ramKB = float(format(ramInfo['MemFree']).split(' ')[0])
        ramGB = ramKB/1024/1024
        ramGB = round(ramGB)
        return ramGB
    
    def size(self, device):
        
        nr_sectors = open(device+'/size').read().rstrip('\n')
        sect_size = open(device+'/queue/hw_sector_size').read().rstrip('\n')

        # The sect_size is in bytes, so we convert it to GiB and then send it back
        return (float(nr_sectors)*float(sect_size))/(1024.0*1024.0*1024.0)

    def getTotalDiskSpace(self):
        
        dev_pattern = ['sd.*','mmcblk*']
        
        for device in glob.glob('/sys/block/*'):
            for pattern in dev_pattern:
                if re.compile(pattern).match(os.path.basename(device)):
                    #print('Device:: {0}, Size:: {1} GiB'.format(device, self.size(device)))
                    totalSpace = format(self.size(device))
                    x = float(totalSpace) * 1024 * 1024 
                    return totalSpace
                
    def getFreeDiskSpace(self):
        
        s = os.statvfs('/')
        freeSpace = float(float((s.f_bavail * s.f_frsize)) / 1024)
        freeSpaceGB = float(freeSpace / 1024 / 1024)
        return freeSpaceGB
        
    def getCpuUsage(self):
        
        dt = self.deltaTime(self.interval)
        cpuPct = 100 - (dt[len(dt) - 1] * 100.00 / sum(dt))
        
        return str('%.4f' %cpuPct)
    
    def getTimeList(self):
        
        statFile = file("/proc/stat", "r")
        timeList = statFile.readline().split(" ")[2:6]
        statFile.close()
        
        for i in range(len(timeList))  :
            timeList[i] = int(timeList[i])
        
        return timeList

    def deltaTime(self,interval)  :
        
        x = self.getTimeList()
        time.sleep(interval)
        y = self.getTimeList()
        
        for i in range(len(x))  :
            y[i] -= x[i]
        
        return y
    
    def getLocation(self):
        
        ret = urllib2.urlopen('https://enabledns.com/ip')
        ip = ret.read()

        FREEGEOPIP_URL = 'http://freegeoip.net/json/'

        url = '{}/{}'.format(FREEGEOPIP_URL, ip)

        response = requests.get(url)
        response.raise_for_status()

        return response.json()
    