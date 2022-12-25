adminRouterData = [
        {
            "name": "System",
            "path": "/system",
            "hidden": False,
            "redirect": "noRedirect",
            "component": "Layout",
            "alwaysShow": True,
            "meta": {
                "title": "系统管理",
                "icon": "system",
                "noCache": False,
                "link": None
            },
            "children": [
                {
                    "name": "User",
                    "path": "user",
                    "hidden": False,
                    "component": "system/user/index",
                    "meta": {
                        "title": "用户管理",
                        "icon": "user",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Tag",
                    "path": "tag",
                    "hidden": False,
                    "component": "manage/tag/index",
                    "meta": {
                        "title": "标签管理",
                        "icon": "dict",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Post",
                    "path": "post",
                    "hidden": False,
                    "component": "manage/post/index",
                    "meta": {
                        "title": "帖子管理",
                        "icon": "dict",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Visualization",
                    "path": "visualization",
                    "hidden": False,
                    "component": "manage/visualization/index",
                    "meta": {
                        "title": "可视化界面",
                        "icon": "tree",
                        "noCache": False,
                        "link": None
                    }
                },
            ]
        },
        {
            "name": "Monitor",
            "path": "/monitor",
            "hidden": False,
            "redirect": "noRedirect",
            "component": "Layout",
            "alwaysShow": True,
            "meta": {
                "title": "系统监控",
                "icon": "monitor",
                "noCache": False,
                "link": None
            },
            "children": [
                {
                    "name": "Online",
                    "path": "online",
                    "hidden": False,
                    "component": "monitor/online/index",
                    "meta": {
                        "title": "在线用户",
                        "icon": "online",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Server",
                    "path": "server",
                    "hidden": False,
                    "component": "monitor/server/index",
                    "meta": {
                        "title": "服务监控",
                        "icon": "server",
                        "noCache": False,
                        "link": None
                    }
                },
            ]
        },
        {
            "name": "MOOC数据库系统概论",
            "path": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_",
            "hidden": False,
            "component": "Layout",
            "meta": {
                "title": "MOOC数据库系统概论",
                "icon": "guide",
                "noCache": False,
                "link": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_"
            }
        }
    ]


taggerRouterData = [
        {
            "name": "System",
            "path": "/system",
            "hidden": False,
            "redirect": "noRedirect",
            "component": "Layout",
            "alwaysShow": True,
            "meta": {
                "title": "系统管理",
                "icon": "system",
                "noCache": False,
                "link": None
            },
            "children": [
                {
                    "name": "Tag",
                    "path": "tag",
                    "hidden": False,
                    "component": "manage/tag/index",
                    "meta": {
                        "title": "标签管理",
                        "icon": "dict",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Post",
                    "path": "post",
                    "hidden": False,
                    "component": "manage/post/index",
                    "meta": {
                        "title": "帖子管理",
                        "icon": "dict",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Visualization",
                    "path": "visualization",
                    "hidden": False,
                    "component": "manage/visualization/index",
                    "meta": {
                        "title": "可视化界面",
                        "icon": "tree",
                        "noCache": False,
                        "link": None
                    }
                },
            ]
        },
        {
            "name": "MOOC数据库系统概论",
            "path": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_",
            "hidden": False,
            "component": "Layout",
            "meta": {
                "title": "MOOC数据库系统概论",
                "icon": "guide",
                "noCache": False,
                "link": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_"
            }
        }
    ]

commonRouterData = [
        {
            "name": "System",
            "path": "/system",
            "hidden": False,
            "redirect": "noRedirect",
            "component": "Layout",
            "alwaysShow": True,
            "meta": {
                "title": "系统管理",
                "icon": "system",
                "noCache": False,
                "link": None
            },
            "children": [
                {
                    "name": "Tag",
                    "path": "tag",
                    "hidden": False,
                    "component": "manage/tag/index",
                    "meta": {
                        "title": "标签管理",
                        "icon": "dict",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Post",
                    "path": "post",
                    "hidden": False,
                    "component": "manage/post/index",
                    "meta": {
                        "title": "帖子管理",
                        "icon": "dict",
                        "noCache": False,
                        "link": None
                    }
                },
                {
                    "name": "Visualization",
                    "path": "visualization",
                    "hidden": False,
                    "component": "manage/visualization/index",
                    "meta": {
                        "title": "可视化界面",
                        "icon": "tree",
                        "noCache": False,
                        "link": None
                    }
                },
            ]
        },
        {
            "name": "MOOC数据库系统概论",
            "path": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_",
            "hidden": False,
            "component": "Layout",
            "meta": {
                "title": "MOOC数据库系统概论",
                "icon": "guide",
                "noCache": False,
                "link": "https://www.icourse163.org/course/RUC-488001?from=searchPage&outVendor=zw_mooc_pcssjg_"
            }
        }
    ]