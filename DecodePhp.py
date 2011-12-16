#encoding=utf-8
import re
import base64
import string
import os

olddir=r"E:\www\www"
newdir=r"E:\www\www\newfiles"

def SaveFile(name,content):
    if os.path.exists(newdir)==False:
        os.makedirs(newdir)
    filepath = os.path.join(newdir,name)
    write = open(filepath,"w")
    write.write(content)
    write.close()
    print name, " 解密成功！"
def DecodeBase64(oldfile, newfilename):
    listContent = []
    read = open(oldfile,"r")
    line =read.readline()
    while line:
        listContent.append(line)
        line = read.readline()
    read.close()
    #第一次base64解密
    strContent = listContent[1]
    patternStr = "O0O0000O0\('.*'\)"
    match = re.search(patternStr,strContent)
    content=''
    if match:
        content = match.group(0).replace("O0O0000O0('","")
        content = content.replace("')","")
        content = base64.decodestring(content)
     
    #第一次base64解密后的内容查找密钥
    patternStr = "\),'.*',"
    match = re.search(patternStr,content)
    decode_key=''
    if match:
        decode_key = match.group(0).replace("),'","")
        decode_key = decode_key.replace("',","")
    #查找要截取字符串长度
    patternStr = ",\d*\),"
    match = re.search(patternStr,content)
    str_length = ''
    if match:
        str_length = match.group(0).replace("),","")
        str_length = str_length.replace(",","")
        
    #截取文件加密后的密文
    secret = listContent[2][int(str_length):]
    #还原密文输出
    result = secret.translate(string.maketrans(decode_key, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="))
    result = "<?php\n"+base64.decodestring(result)+"?>"
    SaveFile(newfilename,result)
    
def GetPhpFiles(dirname):
    filenames = os.listdir(dirname)
    for name in filenames:
        filepath = os.path.join(dirname,name)
        if os.path.isfile(filepath) and filepath.find(".php",0)>-1:
            DecodeBase64(filepath,name)
            
if __name__ == "__main__":
    GetPhpFiles(olddir)

