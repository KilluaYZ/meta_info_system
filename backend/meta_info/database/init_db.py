from flask import Flask
from flask import request
from flask import Blueprint
from flask import current_app, g
from flask.cli import with_appcontext
import os
import sys
import click

import meta_info.database.connectPool
global pooldb
pooldb = meta_info.database.connectPool.pooldb

def init_db():
    print("开始创建数据库")
    pooldb.execute_scirpt('meta_info/database/init.sql')
    

