from flask import Flask
from flask import request
from flask import Blueprint
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from database.connect import Conndb

tag = Blueprint('tag',__name__)
conndb = Conndb()

@tag.route('/add', methods=['POST'])
def addTag():
    # if request.method == 'POST':
    #     sql = request.json.get('sql')
    # else:
    #     sql = request.args.get('sql')
    # print(sql)
    # data = conndb.read(sql)
    # return str(data)
    
