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

const HotTagsData = {
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
    ]
}

const NewTagsData = {
    code : 200,
    msg : "操作成功",
    data : [
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

const HotPostsData = {
    code : 200,
    msg : "操作成功",
    data: [
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容1",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容2",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容3",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容4",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容5的按本地阿布ui悲催啊不i吧uia吧挠啊从啊擦拭啊啊的安布ui百度擦ui并处于边缘v元v创意图vact有从v天涯从天涯和长白班uiab与擦u余元v从元v粗与阿姨v冲压v元v与阿姨v与擦v与v啊va",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        }
    ]   

}

const NewPostsData = {
    code : 200,
    msg : "操作成功",
    data: [
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容6",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容7",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容8",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容9",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        },
        {
            postTitle:"帖子标题",
            postKeywords:[
                "关键词1",
                "关键词2",
                "关键词3",
            ],//一个帖子有多个关键词,
            postTag:["1","2","3"],
            postContent:"帖子内容10",
            postTime:{
                year:2022,
                month:12,
                day:6
                //目前就精确到日，因为没必要到时分秒
            },
            postAnswer:"回答",
            postPopularity:666
        }
    ]   
}

export function getMockHotTags(queryParam) {
    let returnData = undefined 
    if(queryParam.HotTagsNum == 5){
        returnData = HotTagsData;
    }

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(returnData)
        }, 100)
    })
}

export function getMockNewTags(queryParam) {
    let returnData = undefined 
    if(queryParam.NewTagsNum == 5){
        returnData = NewTagsData;
    }

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(returnData)
        }, 100)
    })
}

export function getMockHotPosts(queryParam) {
    let returnData = undefined 
    if(queryParam.HotPostsNum == 5){
        returnData = HotPostsData;
    }

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(returnData)
        }, 100)
    })
}

export function getMockNewPosts(queryParam) {
    let returnData = undefined 
    if(queryParam.NewPostsNum == 5){
        returnData = NewPostsData;
    }

    return new Promise((resolve, reject) => {
        setTimeout(() => {
            resolve(returnData)
        }, 100)
    })
}