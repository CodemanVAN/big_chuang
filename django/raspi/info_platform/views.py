from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
import time

def show_pi_info(request):
    info=get_all_info()
    return render(request, "info_platform.html", info)  

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
 
# Return RAM information (unit=kb) in a list                                       
# Index 0: total RAM                                                               
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 
# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
 
# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                         
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
 
 

def get_all_info():
    # CPU informatiom
    CPU_temp = getCPUtemperature()
    CPU_usage = getCPUuse()
    
    # RAM information
    # Output is in kb, here I convert it in Mb for readability
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    RAM_free = round(int(RAM_stats[2]) / 1000,1)
    
    # Disk information
    DISK_stats = getDiskSpace()
    DISK_total = DISK_stats[0]
    DISK_used = DISK_stats[1]
    DISK_perc = DISK_stats[3]
    info={}
    info['CPU_Temperature']=CPU_temp
    info['CPU_Use']=CPU_usage
    info['RAM_total']=str(RAM_total)+' MB'
    info['RAM_Used']=str(RAM_used)+' MB'
    info['RAM_Free']=str(RAM_free)+' MB'
    info['DISK_Total_Space']=str(DISK_total)+'B'
    info['DISK_Used_Space']=str(DISK_used)+'B'
    info['DISK_Used_Percentage']=str(DISK_perc)
    return info
