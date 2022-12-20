'''
该文件包含的函数主要功能是构造response
'''
import json

def build_response(code:int,msg:str,data={},length=0):
    return json.dumps({'code':code,'msg':msg,'data':data,'length':length})

def build_error_response():
    return build_response(400,'操作失败')

def build_success_response(data={},length=0):
    return build_response(200,'操作成功',data,length)

def build_404_response():
    build_response(404,'不存在')