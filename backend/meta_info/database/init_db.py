from flask import Flask
from flask import request
from flask import Blueprint
from flask import current_app, g

import os
import sys

# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from database.connect import Conndb
