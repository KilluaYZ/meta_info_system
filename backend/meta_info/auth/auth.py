from flask import request
from flask import Blueprint
import os
import sys
import inspect

from sqlalchemy import false, null, true


# 找到model文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# sys.path.append("..")

from manage.buildResponse import build_response,build_success_response,build_error_response
from utils.check import is_number
from database.connect import Conndb
from manage.tagManage import query_sql,update_sql

# conndb = Conndb(cursor_mode='dict')
auth = Blueprint('auth', __name__)

import database.connectPool
global pooldb
pooldb = database.connectPool.pooldb

routerData = [
        {
            "name": "System",
            "path": "/system",
            "hidden": false,
            "redirect": "noRedirect",
            "component": "Layout",
            "alwaysShow": true,
            "meta": {
                "title": "系统管理",
                "icon": "system",
                "noCache": false,
                "link": null
            },
            "children": [
                {
                    "name": "User",
                    "path": "user",
                    "hidden": false,
                    "component": "system/user/index",
                    "meta": {
                        "title": "用户管理",
                        "icon": "user",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Tag",
                    "path": "tag",
                    "hidden": false,
                    "component": "manage/tag/index",
                    "meta": {
                        "title": "标签管理",
                        "icon": "dict",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Post",
                    "path": "post",
                    "hidden": false,
                    "component": "manage/post/index",
                    "meta": {
                        "title": "帖子管理",
                        "icon": "dict",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Visualization",
                    "path": "visualization",
                    "hidden": false,
                    "component": "manage/visualization/index",
                    "meta": {
                        "title": "可视化界面",
                        "icon": "tree",
                        "noCache": false,
                        "link": null
                    }
                },
            ]
        },
        {
            "name": "Monitor",
            "path": "/monitor",
            "hidden": false,
            "redirect": "noRedirect",
            "component": "Layout",
            "alwaysShow": true,
            "meta": {
                "title": "系统监控",
                "icon": "monitor",
                "noCache": false,
                "link": null
            },
            "children": [
                {
                    "name": "Online",
                    "path": "online",
                    "hidden": false,
                    "component": "monitor/online/index",
                    "meta": {
                        "title": "在线用户",
                        "icon": "online",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Server",
                    "path": "server",
                    "hidden": false,
                    "component": "monitor/server/index",
                    "meta": {
                        "title": "服务监控",
                        "icon": "server",
                        "noCache": false,
                        "link": null
                    }
                },
            ]
        },
        {
            "name": "MOOC数据库系统概论",
            "path": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_",
            "hidden": false,
            "component": "Layout",
            "meta": {
                "title": "MOOC数据库系统概论",
                "icon": "guide",
                "noCache": false,
                "link": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_"
            }
        }
    ]

@auth.route('/getRouters', methods=['GET'])
def getRouters():
    return build_success_response(routerData)

#收到用户名密码，返回会话对应的toKen
@auth.route('/login', methods=['POST'])
def login():

    return build_success_response()

#获取用户的详细信息
@auth.route('/getInfo', methods=['POST'])
def getInfo():

    return build_success_response()

