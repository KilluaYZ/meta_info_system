# Filename : backendmain.py
# Author by : Qinliang Xue
# Date : 2022-11-14

from flask import Flask
from flask import request
from flask import Blueprint

bp = Blueprint('bp',__name__)

@bp.route('/')
def show():
    return 'bp.hello'