# Filename : backendmain.py
# Author by : Qinliang Xue
# Date : 2022-11-14

from flask import Flask
from flask import request
from flask import Blueprint
import os
import sys
# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from database.connect import Conndb

db = Blueprint('db',__name__)
conndb = Conndb()

@db.route('/', methods=['GET', 'POST'])
def show10():
    if request.method == 'POST':
        sql = request.json.get('sql')
    else:
        sql = request.args.get('sql')
    print(sql)
    data = conndb.read(sql)
    return str(data)