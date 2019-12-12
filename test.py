
# -*- coding: UTF-8 -*-


import os,sys
from jiaowuchu import jw
import json
import string
import random
from mysql import connect,select,zc,relogin,redata,finddata,forget,puttask,prepos,findtask,taskhistory,taskreceived,searchtask,managetask,historytask,upload_img,searchentry,intoken,retoken,draw,restatic,revisepasswd
import requests
#from flask_cors import *
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from flask import Flask ,request,make_response
from flask_wtf.file import FileField, FileRequired, FileAllowed
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
def is_ustr(in_str):
    out_str=''
    for i in range(len(in_str)):
        if is_uchar(in_str[i]):
            out_str=out_str+in_str[i]
        else:
            out_str=out_str+' '
    return out_str
def is_uchar(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            return False
    else:
        return True
@app.route('/test', methods=['get','post'])#cesi
def hello():
    user = request.args.get('user')
    print(user)
    user1 = request.json.get('user1')
    print(user1)
    user2=user1+user
    return user2

@app.route('/regester', methods=[ 'POST'])#注册
def regestertest():
    user = request.json.get('user')
    password = request.json.get('password')
    jwaccount = request.json.get('jwaccount')
    jwpasswd = request.json.get('jwpasswd')
    flag1 = jw(jwaccount, jwpasswd)
    if flag1 == '1000':
        flag = zc(user, password, jwaccount)
        return flag
    else:
        flag = '4003'
        text = {
            'result':flag,

        }

        result=json.dumps(text, ensure_ascii=False)
        return result


@app.route('/login', methods=[ 'POST'])#登入

def logintest():

    user = request.json.get('user')
    password = request.json.get('password')
    result1 = logincontent(user,password)
    text = {
        'result': result1,

    }
    result1 = json.dumps(text, ensure_ascii=False)
    return result1

def logincontent(user,password):
    flag=relogin(user,password)
    if flag!='4005':
        flag=intoken(flag)
    return flag
@app.route('/forget',methods=['POST'])#密码找回
def forgettest():
    jwaccount=request.json.get('jwaccount')
    jwpasswd = request.json.get('jwpasswd')
    flag1 = jw(jwaccount, jwpasswd)
    if flag1 == '1000':
        result2=forget(jwaccount)
        return result2
    else:
        flag1='4003'
        text = {
            'result': flag1,

        }
        result2 = json.dumps(text, ensure_ascii=False)
        return result2

@app.route('/data', methods=[ 'POST'])
def datatest():
    accountname = request.json.get('accountname')
    room = request.json.get('room')
    qq = request.json.get('qq')
    weixin = request.json.get('weixin')
    tele=request.json.get('tele')
    jwac=request.json.get('jwac')
    jwac=retoken(jwac)
    result3 =redata(accountname,room,qq,weixin,tele,jwac)
    return result3

@app.route('/finddata', methods=[ 'POST'])
def finddatatest():
    jwac=request.json.get('jwaccount')
    jwac = retoken(jwac)
    text =finddata(jwac)
    return text

@app.route('/puttask', methods=[ 'POST'])#任务管理
def puttasktest():
    jwac = request.json.get('jwac')
    tno=request.json.get('tno')#创建或查找tno默认为空
    title=request.json.get('title')
    label=request.json.get('label')
    content=request.json.get('content')
    method=str(request.json.get('method'))
    cost=request.json.get('cost')
    num = request.json.get('num')
    date = request.json.get('date')
    flag = request.json.get('flag')
    jwac = retoken(jwac)
    result4=puttask(jwac,tno,title,label,content,method,cost,num,date,flag)
    return result4


@app.route('/prepos', methods=[ 'POST'])#顶置任务或者二手交易
def prepositiontest():
    jwac = request.json.get('jwac')
    tno = request.json.get('tno')
    jwac = retoken(jwac)
    result6=prepos(jwac,tno)
    return result6

@app.route('/findtask', methods=[ 'POST'])#查询任务列表
def findtasktest():
    label=request.json.get('label')
    result7=findtask(label)
    return result7



@app.route('/findtaskhistory', methods=[ 'POST'])#查询历史发布列表
def findtaskhistory():
    jwac=request.json.get('jwac')
    jwac = retoken(jwac)
    result9=taskhistory(jwac)
    return result9



@app.route('/taskreceived', methods=[ 'POST'])#接受任务
def taskreceviedtest():
    jwac=request.json.get('jwac')
    tno=request.json.get('tno')
    jwac = retoken(jwac)
    result11=taskreceived(jwac,tno)
    return result11

@app.route('/searchtask', methods=[ 'POST'])#查询接受任务列表
def searchtasktest():
    jwac=request.json.get('jwac')
    jwac = retoken(jwac)
    result11=searchtask(jwac)
    return result11

@app.route('/managetask', methods=[ 'POST'])#查询接受任务列表
def managetasktest():
    jwac=request.json.get('jwac')
    tno = request.json.get('tno')
    type = request.json.get('type')
    jwac = retoken(jwac)
    result12=managetask(jwac,tno,type)
    return result12


@app.route('/historytask', methods=[ 'POST'])#查询接受任务列表
def historytasktest():
    jwac=request.json.get('jwac')
    jwac = retoken(jwac)
    result13=historytask(jwac)
    return result13

@app.route('/img_upload',methods=['POST'])
def editorData():
    # 获取图片文件 name = upload
    img = request.files.get('upload')
    jwac = request.form.get('jwac')
    type = request.form.get('type')
    jwac = retoken(jwac)
    # 定义一个图片存放的位置 存放在static下面

    path=sys.path[0]+'/img/'

    # 图片名称

    imgName0 =img.filename
    #print(imgName)
    num = 15
    tt = ''.join(random.sample(string.ascii_letters + string.digits, num))#随机生成15位
    imgName=tt+imgName0
    # 图片path和名称组成图片的保存路径
    imgName = imgName.replace(' ', '')  # 取出所有空格
    file_path = path +imgName

    # 保存图片

    img.save(file_path)

    # url是图片的路径

    url ='missionhelp.club:8080/images/'+imgName
    result14 = upload_img(url, jwac, type)
    return result14
    #return url


'''
@app.route('/img_upload',methods=['POST'])
def editorData():
    #flask前端与后端之间传递的两种数据格式：json与FormData
    img = request.files.get('upload')
    jwac =request.form.get('jwac')
    type=request.form.get('type')
    jwac = retoken(jwac)
    # 定义一个图片存放的位置 存放在static下面

    path='D:\\server/img/'

    # 图片名称

    imgName0 = is_ustr(img.filename)
    #print(imgName)
    num = 15
    tt = ''.join(random.sample(string.ascii_letters + string.digits, num))#随机生成15位
    imgName=tt+imgName0
    # 图片path和名称组成图片的保存路径
    imgName = imgName.replace(' ', '')  # 取出所有空格
    file_path = path +imgName

    # 保存图片

    img.save(file_path)

    # url是图片的路径
    #发包到图库
    url = 'https://sm.ms/api/upload'
    file_obj = open(file_path, 'rb')
    file = {'smfile': file_obj}  # 参数名称必须为smfile
    data_result = requests.post(url, data=None, files=file)
    data = data_result.json()
    #print(data_result.json())  # 得到json结果
    flag = data['code']
    if flag == 'image_repeated':
        img = data['images']
    elif flag == 'success':
        img = data['data']['url']
    else:
        img = 'Flase'
    print(img)
    url =img
    result14 = upload_img(url,jwac,type)
    return result14
    #return url
    '''

@app.route('/searchentry', methods=[ 'POST'])#查询接受任务列表
def searchentry0():
    entry=request.json.get('entry')
    jwac=request.json.get('jwac')
    jwac = retoken(jwac)
    result15=searchentry(entry)
    return result15

@app.route('/draw', methods=[ 'POST'])#查询任务领取情况
def drawtest():
    tno=request.json.get('tno')
    jwac=request.json.get('jwac')
    jwac=retoken(jwac)
    result16=draw(tno,jwac)
    return result16
@app.route('/static', methods=[ 'POST'])#查询任务领取情况
def findStatic():
    jwac=request.json.get('jwac')
    result17=restatic(jwac)
    return result17
@app.route('/revisepasswd', methods=[ 'POST'])#查询任务领取情况
def passwd():
    jwac=request.json.get('jwac')
    passwd = request.json.get('passwd')
    newpasswd=request.json.get('newpasswd')
    jwac = retoken(jwac)
    result17=revisepasswd(jwac,passwd,newpasswd)
    return result17


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
    #app.run(host='192.168.43.10', port=5590)
