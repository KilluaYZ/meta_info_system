import platform
from psutil import *
import socket
 
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        
    return ip
def getPlantformInfo():
    cpu_used = cpu_percent(interval=2)
    cpu_free = 100.0 - cpu_used
    mem_info = virtual_memory()
    
    res = {
        "cpu":{
            "cpuType":str(platform.processor()),
            "used":str(cpu_used),
            "free":str(cpu_free)
        },
        "mem":{
            "total": "%.2f" % (mem_info[0]/(float)(1024*1024*1024)),
            "used": "%.2f" % (mem_info[3]/(float)(1024*1024*1024)),
            "free": "%.2f" % (mem_info[4]/(float)(1024*1024*1024)),
            "usage": "%.2f" % (mem_info[2])
        },
        "sys": {
            "computerName": str(platform.node()),
            "computerIp": str(get_host_ip()),
            "osName": str(platform.platform()),
            "osArch": str(platform.machine())
        }
    }
    
