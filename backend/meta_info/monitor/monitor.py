import platform
from psutil import *
import socket
from flask import request
from flask import Blueprint
import os
import sys
import inspect

# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.buildResponse import *
from utils.check import is_number
monitor = Blueprint('monitor', __name__)
from auth.auth import get_user_by_token

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        
    return ip

@monitor.route('/server', methods=['GET'])
def getPlantformInfo():
    try:
        token = request.headers.get('Authorization')
        if token is None:
            raise Exception('token不存在，无法查询')
        user = get_user_by_token(token)
        if user is None:
            raise Exception('未登录无法查询')
        
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
        return build_success_response(res)
    
    except Exception as e:
        print("[ERROR]"+__file__+"::"+inspect.getframeinfo(inspect.currentframe().f_back)[2])
        print(e)
        return build_error_response()
        