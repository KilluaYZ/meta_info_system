#对文件进行base64编码，解码
import base64
import os

def encode_base64(file):
    with open(file,'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        return base64_data

def decode_base64(file,base64_data):
    with open(file,'wb') as f:
        img = base64.b64decode(base64_data)
        f.write(img)