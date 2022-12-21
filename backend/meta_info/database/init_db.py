from database.connect import Conndb
from flask import Flask
from flask import request
from flask import Blueprint
from flask import current_app, g
from flask.cli import with_appcontext
import os
import sys
import click

# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# sys.path.append(".")
# sys.path.append("..")
conndb = Conndb()


def init_db():
    print("开始创建数据库")
    conndb.execute_scirpt('database/init.sql')
    

