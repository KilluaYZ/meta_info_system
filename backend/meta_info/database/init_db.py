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
from database.connect import Conndb
conndb = Conndb()

def init_db():
    with current_app.open_resource('init.sql') as f:
        conndb.write(f.read().decode('utf8'))
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    '''删除现有的所有数据，并新建关系表'''
    init_db()
    click.echo("Initialized the database.")
    


