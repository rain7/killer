
# -*- coding: UTF-8 -*-


import os
from jiaowuchu import jw
import json
from mysql import connect,select,zc,relogin,redata,finddata,forget,puttask
#from flask_cors import *

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

from flask import Flask ,request
from flask_wtf.file import FileField, FileRequired, FileAllowed

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/regester', methods=[ 'POST'])
def regestertest():
    user = request.json.get('user')
    password = request.json.get('password')
    jwaccount = request.json.get('jwaccount')
    jwpasswd = request.json.get('jwpasswd')
    result = regestercontent(user,password,jwaccount,jwpasswd)
    return result

def regestercontent(user,password,jwaccount,jwpasswd):
    flag1=jw(jwaccount,jwpasswd)
    if flag1=='1000':
        flag=zc(user,password,jwaccount)
    else:
        flag='3001'
    return flag

@app.route('/login', methods=[ 'POST'])

def logintest():

    user = request.json.get('user')
    password = request.json.get('password')
    result1 = logincontent(user,password)
    return result1

def logincontent(user,password):
    username,passwd,jwaccount=relogin(user,password)
    len0=len(username)
    flag='4001'
    for i in range(0,len0):
        if user==username[i] and password==passwd[i]:
            jwac=jwaccount[i]
            flag=jwac
    return flag
@app.route('/forget',methods=['POST'])
def forgettest():
    user=request.json.get('user')
    jwaccount=request.json.get('jwaccount')
    result2=forget(user,jwaccount)
    return result2

@app.route('/data', methods=[ 'POST'])
def datatest():
    accountname = request.json.get('accountname')
    room = request.json.get('room')
    qq = request.json.get('qq')
    weixin = request.json.get('weixin')
    jwac=request.json.get('jwac')
    result3 =redata(accountname,room,qq,weixin,jwac)
    return result3

@app.route('/finddata', methods=[ 'POST'])
def finddatatest():
    jwac=request.json.get('jwaccount')
    text =finddata(jwac)
    return text

@app.route('/puttask', methods=[ 'POST'])
def puttasktest():
    jwac = request.json.get('jwac')
    title=request.json.get('title')
    label=request.json.get('label')
    content=request.json.get('content')
    method=request.json.get('method')
    result4=puttask(jwac,title,label,content,method)


###



if __name__ == '__main__':

    app.run(host='172.26.78.22', port=5590)
    ''''''
