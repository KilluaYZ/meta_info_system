from setuptools import find_packages, setup

setup(
    name='meta_info',
    version='1.1.0',
    packages=[
        'meta_info',
        'meta_info.auth',
        'meta_info.database',
        'meta_info.mainpage',
        'meta_info.manage',
        'meta_info.utils',
        'meta_info.monitor',
        ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'PyMySql',
        'flask_cors',
        'sqlalchemy',
        'DButils',
        'wordcloud',
        'psutil',
        'flask_apscheduler'
    ],
)