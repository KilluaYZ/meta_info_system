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
            tagClass: 1,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名2",
            tagID: "2",
            tagClass: 3,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名3",
            tagID: "3",
            tagClass: 2,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名4",
            tagID: "4",
            tagClass: 2,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名5",
            tagID: "5",
            tagClass: 1,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名6",
            tagID: "6",
            tagClass: 1,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名7",
            tagID: "7",
            tagClass: 3,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名8",
            tagID: "8",
            tagClass: 1,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名9",
            tagID: "9",
            tagClass: 1,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        },
        {
            tagName: "标签名10",
            tagID: "10",
            tagClass: 1,
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注我是谁吉萨的看法化解了安徽省价格很绝望感觉哈桑了的回顾 活塞i干哈就开始了规划爱上了规划i是党和国家啊是的贵啊和山地和  和世界观和俺家帅哥洒家扩大规划叫阿三的哈公司电话挂机啊说得好叫阿三的和健康噶说的话九阿哥合适的金克拉更合适的"
        },
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
            tagClass: "2",
            tagParentName: "父标签名",
            tagPopularity: 666,
            remark: "备注"
        }
    ]
}

export function getMockTagData(queryParam) {
    let returnData = undefined;
    if (queryParam.tagName != undefined) {
        console.log('查询tagName')
        returnData = TagNameTagData;
    } else if (queryParam.tagID != undefined) {
        console.log('查询tagID')
        returnData = TagIDTagData;
    } else {
        console.log('查询所有tag数据')
        returnData = AllTagData;
    }

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(returnData)
        }, 100)
    })
}

const AllPostData = {
    code: 200,
    msg: "操作成功",
    data: [
        {
            postID: "123",
            postTitle: "帖子标题1",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容1",
            postTime: "2022-12-13",
            postAnswer:"回答1",
            postPopularity: 666,
            remark: "备注1"
        },
        {
            postID: "123",
            postTitle: "帖子标题2",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容2",
            postTime: "2022-12-13",
            postAnswer:"回答1",
            postPopularity: 666,
            remark: "备注2"
        },
        {
            postID: "123",
            postTitle: "帖子标题3",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容3",
            postTime: "2022-12-13",
            postAnswer:"回答1",
            postPopularity: 666,
            remark: "备注3"
        },
        {
            postID: "123",
            postTitle: "帖子标题4",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容4",
            postTime: "2022-12-13",
            postAnswer:"回答1",
            postPopularity: 666,
            remark: "备注4"
        },
        {
            postID: "123",
            postTitle: "帖子标题5",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容5",
            postTime: "2022-12-13",
            postAnswer:"回答1",
            postPopularity: 666,
            remark: "备注5"
        },
        {
            postID: "123",
            postTitle: "帖子标题6",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容1",
            postTime: "2022-12-13",
            postAnswer:"回答6",
            postPopularity: 666,
            remark: "备注6"
        },
        {
            postID: "123",
            postTitle: "帖子标题7",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容7",
            postTime: "2022-12-13",
            postAnswer:"回答1",
            postPopularity: 666,
            remark: "备注7"
        },
        {
            postID: "123",
            postTitle: "帖子标题8",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容1",
            postTime: "2022-12-13",
            postAnswer:"回答8",
            postPopularity: 666,
            remark: "备注8"
        },
        {
            postID: "123",
            postTitle: "帖子标题9",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容9",
            postTime: "2022-12-13",
            postAnswer:"回答9",
            postPopularity: 666,
            remark: "备注9"
        },
        {
            postID: "123",
            postTitle: "帖子标题10",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容10",
            postTime: "2022-12-13",
            postAnswer:"回答10",
            postPopularity: 666,
            remark: "备注10"
        },
    ],
    length:50

}

const postIDData = {
    code: 200,
    msg: "操作成功",
    data: [
        {
            postID: "123",
            postTitle: "帖子ID标题",
            postKeywords: [
                "关键词1",
                "关键词2",
                "关键词3",
            ],
            postTag: [
                {
                    tagName: "标签名3",
                    tagID: "3",
                    tagClass: "3",
                    tagParentName: "标签名2",
                    tagPopularity: 666,
                    remark: "备注",
                },
            ],
            postContent: "帖子内容1",
            postTime: "2022-12-13",
            postAnswer:"回答1",
            postPopularity: 666,
            remark: "备注1"
        },
    ],
    
}

export function getMockPostData(queryParam) {
    let returnData = undefined;
    if (queryParam.postID != undefined) {
        console.log('查询postID')
        returnData = postIDData;
    } else {
        console.log('查询所有tag数据')
        returnData = AllPostData;
    }

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(returnData)
        }, 100)
    })
}

//修改数据
export const UpdateData = {
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

export const frontTagTreeData = {
    code:200,
    msg:"操作成功",
    data:[
        {
            tagName:"标签名1",
            tagID:"1",
            tagClass:"1",
            tagParentName:null,
            tagPopularity:10,
            remark:"备注",
            type:"danger"
        },
        {
            tagName:"标签名4",
            tagID:"4",
            tagClass:"2",
            tagParentName:"标签名1",
            tagPopularity:666,
            remark:"备注",
            type:"success"
        },                     
    ]
}
