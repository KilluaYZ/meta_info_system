from database.connect import Conndb
from flask import Flask
from flask import request
from flask import Blueprint
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

tag = Blueprint('tag', __name__)
conndb = Conndb()

'''
    重要数据项
    tagName = request.json.get('tagName')
    tagClass = request.json.get('tagClass')
    tagParentName = request.json.get('tagParentName')
    remark = request.json.get('remark')
    tagPopularity = request.json.get('tagPopularity')
'''



@tag.route('/add', methods=['POST'])
def addTag():
    

    return
