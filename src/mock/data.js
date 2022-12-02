export const MenuData = {
    msg: "操作成功",
    data: [
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
                    "name": "Role",
                    "path": "role",
                    "hidden": false,
                    "component": "system/role/index",
                    "meta": {
                        "title": "角色管理",
                        "icon": "peoples",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Menu",
                    "path": "menu",
                    "hidden": false,
                    "component": "system/menu/index",
                    "meta": {
                        "title": "菜单管理",
                        "icon": "tree-table",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Dept",
                    "path": "dept",
                    "hidden": false,
                    "component": "system/dept/index",
                    "meta": {
                        "title": "部门管理",
                        "icon": "tree",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Post",
                    "path": "post",
                    "hidden": false,
                    "component": "system/post/index",
                    "meta": {
                        "title": "岗位管理",
                        "icon": "post",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Dict",
                    "path": "dict",
                    "hidden": false,
                    "component": "system/dict/index",
                    "meta": {
                        "title": "字典管理",
                        "icon": "dict",
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
                    "name": "Config",
                    "path": "config",
                    "hidden": false,
                    "component": "system/config/index",
                    "meta": {
                        "title": "参数设置",
                        "icon": "edit",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Notice",
                    "path": "notice",
                    "hidden": false,
                    "component": "system/notice/index",
                    "meta": {
                        "title": "通知公告",
                        "icon": "message",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Log",
                    "path": "log",
                    "hidden": false,
                    "redirect": "noRedirect",
                    "component": "ParentView",
                    "alwaysShow": true,
                    "meta": {
                        "title": "日志管理",
                        "icon": "log",
                        "noCache": false,
                        "link": null
                    },
                    "children": [
                        {
                            "name": "Operlog",
                            "path": "operlog",
                            "hidden": false,
                            "component": "monitor/operlog/index",
                            "meta": {
                                "title": "操作日志",
                                "icon": "form",
                                "noCache": false,
                                "link": null
                            }
                        },
                        {
                            "name": "Logininfor",
                            "path": "logininfor",
                            "hidden": false,
                            "component": "monitor/logininfor/index",
                            "meta": {
                                "title": "登录日志",
                                "icon": "logininfor",
                                "noCache": false,
                                "link": null
                            }
                        }
                    ]
                }
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
                    "name": "Job",
                    "path": "job",
                    "hidden": false,
                    "component": "monitor/job/index",
                    "meta": {
                        "title": "定时任务",
                        "icon": "job",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Druid",
                    "path": "druid",
                    "hidden": false,
                    "component": "monitor/druid/index",
                    "meta": {
                        "title": "数据监控",
                        "icon": "druid",
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
                {
                    "name": "Cache",
                    "path": "cache",
                    "hidden": false,
                    "component": "monitor/cache/index",
                    "meta": {
                        "title": "缓存监控",
                        "icon": "redis",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "CacheList",
                    "path": "cacheList",
                    "hidden": false,
                    "component": "monitor/cache/list",
                    "meta": {
                        "title": "缓存列表",
                        "icon": "redis-list",
                        "noCache": false,
                        "link": null
                    }
                }
            ]
        },
        {
            "name": "Tool",
            "path": "/tool",
            "hidden": false,
            "redirect": "noRedirect",
            "component": "Layout",
            "alwaysShow": true,
            "meta": {
                "title": "系统工具",
                "icon": "tool",
                "noCache": false,
                "link": null
            },
            "children": [
                {
                    "name": "Build",
                    "path": "build",
                    "hidden": false,
                    "component": "tool/build/index",
                    "meta": {
                        "title": "表单构建",
                        "icon": "build",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Gen",
                    "path": "gen",
                    "hidden": false,
                    "component": "tool/gen/index",
                    "meta": {
                        "title": "代码生成",
                        "icon": "code",
                        "noCache": false,
                        "link": null
                    }
                },
                {
                    "name": "Swagger",
                    "path": "swagger",
                    "hidden": false,
                    "component": "tool/swagger/index",
                    "meta": {
                        "title": "系统接口",
                        "icon": "swagger",
                        "noCache": false,
                        "link": null
                    }
                }
            ]
        },
        {
            "name": "Http://ruoyi.vip",
            "path": "http://ruoyi.vip",
            "hidden": false,
            "component": "Layout",
            "meta": {
                "title": "若依官网",
                "icon": "guide",
                "noCache": false,
                "link": "http://ruoyi.vip"
            }
        }
    ]
};

export const UserData = {
    msg: "操作成功",
    permissions: ["*:*:*"],
    roles: ["admin"],
    user: {
        "searchValue": null,
        "createBy": "admin",
        "createTime": "2022-10-19 20:56:47",
        "updateBy": null,
        "updateTime": null,
        "remark": "管理员",
        "params": {},
        "userId": 1,
        "deptId": 103,
        "userName": "admin",
        "nickName": "若依",
        "email": "ry@163.com",
        "phonenumber": "15888888888",
        "sex": "1",
        "avatar": "",
        "password": "$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2",
        "status": "0",
        "delFlag": "0",
        "loginIp": "114.240.229.211",
        "loginDate": "2022-11-30T18:55:55.000+08:00",
        "dept": {
            "searchValue": null,
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "remark": null,
            "params": {},
            "deptId": 103,
            "parentId": 101,
            "ancestors": "0,100,101",
            "deptName": "研发部门",
            "orderNum": 1,
            "leader": "若依",
            "phone": null,
            "email": null,
            "status": "0",
            "delFlag": null,
            "parentName": null,
            "children": []
        },
        "roles": [
            {
                "searchValue": null,
                "createBy": null,
                "createTime": null,
                "updateBy": null,
                "updateTime": null,
                "remark": null,
                "params": {},
                "roleId": 1,
                "roleName": "超级管理员",
                "roleKey": "admin",
                "roleSort": "1",
                "dataScope": "1",
                "menuCheckStrictly": false,
                "deptCheckStrictly": false,
                "status": "0",
                "delFlag": null,
                "flag": false,
                "menuIds": null,
                "deptIds": null,
                "permissions": null,
                "admin": true
            }
        ],
        "roleIds": null,
        "postIds": null,
        "roleId": null,
        "admin": true
    }
};

export const TookenData = {
    msg: "操作成功",
    token: "eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjEyY2I1MGQ3LTQyZTYtNGQ4NS1hMThiLTU1ZWI2NTlmMDU2NiJ9.gnKM328o3SetmAIE8mpQ0s__3XL66z8xf7YAEP7lLl1zHuYLPNsf-cZDaaWhJzmqyY4za8ZwPGsYy7QaYILiBA"
};



//查询数据
const AllTagData = {
    code: 200,
    msg: "操作成功",
    data: [
        {
            tagName: "标签名",
            tagID: "1",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名2",
            tagID: "2",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名3",
            tagID: "3",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名4",
            tagID: "4",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名5",
            tagID: "5",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名6",
            tagID: "6",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名7",
            tagID: "7",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名8",
            tagID: "8",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名9",
            tagID: "9",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名10",
            tagID: "10",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        }
    ]
}


const TagNameTagData = {
    code: 200,
    msg: "操作成功",
    data: [
        {
            tagName: "标签名NAME",
            tagID: "10",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        }
    ]
}

const TagIDTagData = {
    code: 200,
    msg: "操作成功",
    data: [
        
        {
            tagName: "标签名ID",
            tagID: "10",
            tagClass: "1",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        }
    ]
}

export function getMockTagData(queryParam) {
    let returnData = undefined;
    if(queryParam.tagName != undefined){
        returnData = TagNameTagData;
    }else if(queryParam.tagID != undefined){
        returnData = TagIDTagData;
    }else {
        returnData = AllTagData;
    }

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(returnData)
        }, 100)
    })
}


//修改数据
export const EditData = {
    code: 200,
    msg: "操作成功"
}

//删除数据
export const DelData = {
    code: 200,
    msg: "操作成功"
}

//添加数据
export const AddData = {
    code: 200,
    msg: "操作成功"
}