from flask import Flask
from flask import request
from flask import Blueprint
import json
import os
import sys

# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# sys.path.append("..")

from utils.buildResponse import build_response,build_success_response,build_error_response
from utils.check import is_number
from database.connect import Conndb

