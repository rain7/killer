import pymssql
import json
import time
import datetime
import re
import random
import string
def connect():
    flag = pymssql.connect(host='47.94.231.254', server='47.94.231.254', port='1433', user='sa', password='xxx',
                           database='Account', charset="utf8")
    if flag:
        print("连接成功")
    return flag



def select():
    conn=connect()
    if conn:
        cursor=conn.cursor()#创建游标对象
        sql='select username from account'
        cursor.execute(sql)
        data=cursor.fetchall()
        para = []
        for i in data:

            text = {'name': str(i[0]).strip()}
            print(text)
            para.append(text)
        cursor.close()  # 关闭游标
        conn.close()
        return json.dumps(para, ensure_ascii=False, indent=4)

def zc(user,password,jwaccount):#注册
    conn=connect()
    if conn:
        cursor = conn.cursor()  # 创建游标对象
        try:
            sql = "insert into account(username,passwd,jwaccount) values('%s','%s','%s')  insert into data(jwaccount) values('%s')"%(user,password,jwaccount,jwaccount)
            flag='1000'
            cursor.execute(sql)
            conn.commit()  # 提交修改，不然数据库上不会更新
        except pymssql.IntegrityError:
            flag='4001'
        except pymssql.OperationalError:#数据位溢出
            flag = '4004'

        cursor.close()  # 关闭游标
        conn.close()
    else:
        flag='2001'

    text = {
        'result': flag,

    }

    flag = json.dumps(text, ensure_ascii=False)
    return flag
def relogin(user,passwd):
    conn = connect()
    if conn:
        cursor = conn.cursor()  # 创建游标对象
        sql0 = "select count(*) from account where (username='%s'or jwaccount='%s') and passwd='%s'" % (user,user,passwd)
        cursor.execute(sql0)
        data = cursor.fetchone()
        count = int(data[0])
        if count==1:
            sql0 = "select jwaccount from account where (username='%s'or jwaccount='%s')" % (user,user)
            cursor.execute(sql0)
            data = cursor.fetchone()
            jwac = str(data[0]).strip()
            return jwac
        else:
            return '4005'

def redata(accountname,room,qq,weixin,tele,jwac):
    conn=connect()
    if conn:
        try:
            cursor=conn.cursor()
            sql="update data set accountname='%s',room='%s',qq='%s',weixin='%s',tele='%s' where jwaccount='%s'"%(accountname,room,qq,weixin,tele,jwac)
            cursor.execute(sql)
            conn.commit()
            flag='1000'
        except pymssql.OperationalError:
            flag = '4004'
    else:
        flag='2001'
    text = {
        'result': flag,
    }

    flag = json.dumps(text, ensure_ascii=False)
    return flag

def finddata(jwac):#查询资料
    conn=connect()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "select accountname,room,qq,weixin,tele,url from data where jwaccount='%s'"%jwac
            cursor.execute(sql)
            data = cursor.fetchone()
            text={
                'result':'1000',
                'jwac':jwac,
                'accountname': str(data[0]).strip(),
                'room':str(data[1]).strip(),
                'qq':str(data[2]).strip(),
                'weixin':str(data[3]).strip(),
                'tele':str(data[4]).strip(),
                'url':str(data[5]).strip()
            }

            return json.dumps(text, ensure_ascii=False)
        except TypeError:
            flag='4002'
            text = {
                'result': flag,
                'accountname':'',
                'room': '',
                'qq': '',
                'weixin':'',
                'tele': '',
                'url':''
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag

def forget(jwac):#密码找回
    conn=connect()
    if conn:
        try:
            cursor=conn.cursor()
            sql="select username,passwd from account where jwaccount='%s'"%(jwac)
            cursor.execute(sql)
            data=cursor.fetchone()
            username=str(data[0]).strip()
            passwd = str(data[1]).strip()
            text = {
                'username': username,
                'passwd':passwd
            }

            flag = json.dumps(text, ensure_ascii=False)
            return  flag
        except TypeError:
            flag='4002'
            text = {
                'result': flag,
            }

            flag = json.dumps(text, ensure_ascii=False)
            return flag
def puttask(jwac,tno,title,label,content,method,cost,num,date,tt):
    conn=connect()
    if conn:
        try:
            cursor=conn.cursor()
            if method=='insert':
                taskNum=3
                sql0 = "select limit from account where jwaccount='%s'" % jwac
                cursor.execute(sql0)
                data = cursor.fetchone()
                if len(data)!=0:
                    if data[0]=='1'or data[0]=='2':
                        taskNum=0
                sql0 = "select count(*) from task where jwaccount='%s' and static='1'" % jwac
                cursor.execute(sql0)
                data = cursor.fetchone()
                taskNum0=int(data[0])
                if taskNum0<taskNum:
                    #判断是否有上传图片
                    if tt=='1':
                        sql0 = "select task_url from data where jwaccount='%s'" % jwac
                        cursor.execute(sql0)
                        url = cursor.fetchone()
                        task_url = str(url[0]).strip()
                    else:
                        task_url='null'
                    sql0 = "select accountname,url from data where jwaccount='%s'" % jwac  # 查询用户名
                    cursor.execute(sql0)
                    data = cursor.fetchone()
                    username = str(data[0])
                    url = str(data[1])
                    #print(username)
                    life='2'
                    flag='1'
                    tno=time.strftime("%d%H%M%S", time.localtime())+str(random.randint(10,99))#任务号生成
                    rank = time.strftime("%d%H%M%S", time.localtime())
                    it = re.finditer(r"\d+", date)
                    s = ''
                    for match in it:
                        s = s + str(match.group())
                    s=int(s)

                    gg = label.strip() + ';'
                    p = re.compile('(.+?);')
                    pp = p.findall(gg)
                    len0 = len(pp)
                    if len0==1:
                        label1=pp[0]
                        label2=pp[0]
                    elif len0==0:
                        label1 = ''
                        label2 = ''
                    else:
                        label1=pp[0]
                        label2=pp[1]
                    sql="insert into task values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%s','%s','%s')"%(jwac,tno,title,content,label,username,cost,num,life,date,rank,label1,label2,flag,s,tt,task_url,url)
                    cursor.execute(sql)
                    conn.commit()
                    flag='1001'
                    text = {
                        'result': flag,
                        'list1':[],
                        'list2':{}
                    }
                    flag = json.dumps(text, ensure_ascii=False)
                    return flag
                else:
                    text = {
                        'result': '4014',
                        'list1': [],
                        'list2': {}
                    }
                    flag = json.dumps(text, ensure_ascii=False)
                    return flag
            elif method=='update':#只能修改内容
                sql="update task set content='%s' where tno='%s'"%(content,tno)
                cursor.execute(sql)
                conn.commit()
                flag = '1001'
                text = {
                    'result': flag,
                    'list1': [],
                    'list2': {}
                }
                flag = json.dumps(text, ensure_ascii=False)
                return flag
            elif method=='delete':

                try:
                    if jwac.strip() == '007':
                        sql = "select jwaccount from task where tno='%s'" % tno
                        cursor.execute(sql)
                        data = cursor.fetchone()
                        jwac = str(data[0])
                    sql0 = "select count(*) from task where tno='%s' and jwaccount='%s' " % (
                    tno, jwac)  # 查询用户名
                    cursor.execute(sql0)
                    data = cursor.fetchone()
                    count0 = str(data[0]).strip()
                    if count0=='0':
                        flag='4010'
                    else:
                        sql0 = "select title,cost,content,date,accountname from task where tno='%s' and jwaccount='%s'"% (tno,jwac)  # 查询用户名
                        cursor.execute(sql0)
                        data = cursor.fetchone()
                        title = str(data[0])
                        cost = str(data[1])
                        content = str(data[2])
                        date = str(data[3])
                        accountname=str(data[4])


                        sql="update task set static='0' where tno='%s'"%tno
                        cursor.execute(sql)
                        conn.commit()
                        flag = '1001'

                    text = {
                        'result': flag,
                        'list1': [],
                        'list2': {}
                    }
                    flag = json.dumps(text, ensure_ascii=False)
                except TypeError:
                    flag = '4002'
                    text = {
                        'result': flag,
                        'list1': [],
                        'list2': {}
                    }
                    flag = json.dumps(text, ensure_ascii=False)

                return flag
            elif method=='findmytask':
                sql = "select tno,title,label,cost,num,date,url from task where jwaccount='%s' and static='1' order by rank*1 desc"%jwac
                cursor.execute(sql)#后面不能有conn.commit()，否则提交后无法查询
                data = cursor.fetchall()
                task=[]
                title=[]
                label=[]
                cost=[]
                num=[]
                date=[]
                url=[]
                for i in data:
                    task.append(str(i[0]).strip())
                    title.append(str(i[1]).strip())
                    label.append(str(i[2]).strip())
                    cost.append(str(i[3]).strip())
                    num.append(str(i[4]).strip())
                    date.append(str(i[5]).strip())
                    url.append(str(i[6]).strip())
                len0 = len(title)
                text = []
                for i in range(len0):
                    dd = {
                    'tno': task[i],
                    'title':title[i],
                    'label': label[i],
                    'cost': cost[i],
                    'num': num[i],
                    'date':date[i],
                    'url':url[i]
                    }
                    text = text + [dd]
                text = {
                    'result': '1002',
                    'list1': text,
                    'list2':{}
                }
                return json.dumps(text, ensure_ascii=False)
            elif method=='findcontent':
                try:

                    sql = "select jwaccount,accountname,content,title,label,cost,num,task_url,url from task where tno='%s'" % tno
                    cursor.execute(sql)
                    data = cursor.fetchone()
                    jwac0 = str(data[0]).strip()
                    accountname = str(data[1]).strip()
                    content = str(data[2]).strip()
                    title = str(data[3]).strip()
                    label = str(data[4]).strip()
                    cost = str(data[5]).strip()
                    num = str(data[6]).strip()
                    task_url=str(data[7]).strip()
                    url=str(data[8]).strip()
                    jwac=jwac.strip()
                    if jwac=='007':
                        jwac=jwac0
                    if jwac==jwac0:
                        state='1'#1表示 是自己发布的
                    else:
                        state = '2'  # 2表示 别人发布还没接取
                        sql = "select count(*) from receivedtask where tno='%s' and jwaccount='%s'and static='1'" % (tno,jwac)
                        cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
                        data = cursor.fetchone()
                        #print(data[0])
                        if int(data[0])!=0:
                            state='3'#3表示 已接取还未完成
                        else:
                            sql = "select count(*) from receivedtask where tno='%s' and jwaccount='%s' and static='0'" % (tno, jwac)
                            cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
                            data = cursor.fetchone()
                            #print(data[0])
                            if int(data[0]) != 0:
                                state = '4'#4表示 接取并已完成




                    sql = "select qq,weixin,tele from data where jwaccount='%s'"%jwac0
                    cursor.execute(sql)
                    data = cursor.fetchone()
                    text = {
                        'jwac':jwac0,
                        'accountname':accountname,
                        'qq':str(data[0]).strip(),
                        'weixin':str(data[1]).strip(),
                        'tele':str(data[2]).strip(),
                        'content': content,
                        'title':title,
                        'label':label,
                        'cost':cost,
                        'num':num,
                        'state':state,
                        'task_url':task_url,
                        'url':url
                    }
                    text = {
                        'result': '1003',
                        'list1': [],
                        'list2': text
                    }

                    return json.dumps(text, ensure_ascii=False)
                except TypeError:
                    flag='4002'
                    text = {
                        'result': flag,
                        'list1':[],
                        'list2':{}
                    }
                    return json.dumps(text, ensure_ascii=False)



            else:
                flag='4006'
                text = {
                    'result': flag,
                    'list1': [],
                    'list2': {}
                }

                return json.dumps(text, ensure_ascii=False)

        except pymssql.IntegrityError:
                flag = '4001'
                text = {
                    'result': flag,
                    'list1': [],
                    'list2': {}
                }
                flag = json.dumps(text, ensure_ascii=False)
                return flag
        except TypeError:
            flag = '4009'
            text = {
                'result': flag,
                'list1': [],
                'list2': {}
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag

def prepos(jwac,tno):#置顶
    conn=connect()
    if conn:
        try:
            cursor = conn.cursor()
            xno = time.strftime("%m%d%H%M%S", time.localtime())
            sql = "select life from task  where tno='%s'" % tno
            cursor.execute(sql)
            data = cursor.fetchone()
            life=int(data[0].strip())
            if jwac.strip() == '007':
                sql0 = "select jwaccount from task where tno='%s'" % tno
                cursor.execute(sql0)
                data = cursor.fetchone()
                jwac = str(data[0])
                life=1
            if life==0:
                flag = '4011'
                text = {
                    'result': flag
                }
            else:
                sql = "update task set rank='%s' where tno='%s' and jwaccount='%s'" % (xno,tno,jwac)
                cursor.execute(sql)
                conn.commit()
                sql = "update task set life='%s' where tno='%s' and jwaccount='%s'" % (str(life-1),tno,jwac)
                cursor.execute(sql)
                conn.commit()
                flag = '1000'
                text = {
                    'result': flag
                }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
        except pymssql.IntegrityError:
                flag = '4001'
                text = {
                    'result': flag
                }
                flag = json.dumps(text, ensure_ascii=False)
                return flag

def findtask(label): #任务大厅查找任务订单
    conn=connect()
    if conn:
        cursor=conn.cursor()
        try:

            time0 = int(time.strftime("%Y%m%d%H%M", time.localtime()))
            sql = "update task set static='0' where time<='%s'" % time0
            cursor.execute(sql)
            conn.commit()

            if label!='':

                sql="select title,label,accountname,cost,num,tno,date,url from task where (label1='%s'or label2='%s')and num!='0' and static!='0'  order by rank*1 desc"%(label,label)  #tno*1 可以将tno转成int型
                cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
                data = cursor.fetchall()
                title = []
                label=[]
                account=[]
                cost=[]
                num=[]
                tt=[]
                date=[]
                url=[]
                for i in data:
                    title.append(str(i[0]).strip())
                    label.append(str(i[1]).strip())
                    account.append(str(i[2]).strip())
                    cost.append(str(i[3]).strip())
                    num.append(str(i[4]).strip())
                    tt.append(str(i[5]).strip())
                    date.append(str(i[6]).strip())
                    url.append(str(i[7]).strip())
                #print(title, jwac)
                len0=len(title)
                text=[]
                for i in range(len0):
                    dd={
                    'title':title[i],
                    'label':label[i],
                    'accountname': account[i],
                    'cost': cost[i],
                    'num':num[i],
                    'tno': tt[i],
                    'date':date[i],
                    'url':url[i]
                     }
                    text=text+[dd]
                text = {
                    'result': '1000',
                    'list': text
                }

                return json.dumps(text, ensure_ascii=False)
            else:
                sql = "select title,label,accountname,cost,num,tno,date,url from task where num!='0' and static!='0' order by rank*1 desc"  # tno*1 可以将tno转成int型
                cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
                data = cursor.fetchall()
                title = []
                label=[]
                account = []
                cost=[]
                num=[]
                tt=[]
                date=[]
                url=[]
                for i in data:
                    title.append(str(i[0]).strip())
                    label.append(str(i[1]).strip())
                    account.append(str(i[2]).strip())
                    cost.append(str(i[3]).strip())
                    num.append(str(i[4]).strip())
                    tt.append(str(i[5]).strip())
                    date.append(str(i[6]).strip())
                    url.append(str(i[7]).strip())
                #print(title,jwac)
                len0 = len(title)
                text=[]
                for i in range(len0):
                    dd = {
                        'title': title[i],
                        'label':label[i],
                        'accountname': account[i],
                        'cost': cost[i],
                        'num': num[i],
                        'tno': tt[i],
                        'date':date[i],
                        'url':url[i]
                    }

                    text = text + [dd]
                text={
                    'result':'1000',
                    'list':text
                }
                return json.dumps(text, ensure_ascii=False)

        except pymssql.IntegrityError:
            flag = '4001'
            text = {
                'result': flag,
                'list':[]
            }
            return json.dumps(text, ensure_ascii=False)

def taskhistory(jwac):#查询发布历史
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "select tno,title,label,date,cost,url from task where jwaccount='%s' and static='0' order by rank*1 desc"%jwac
            cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
            data = cursor.fetchall()
            tno = []
            title = []
            label = []
            date = []
            cost=[]
            url=[]
            for i in data:
                tno.append(str(i[0].strip()))
                title.append(str(i[1]).strip())
                label.append(str(i[2]).strip())
                date.append(str(i[3]).strip())
                cost.append(str(i[4]).strip())
                url.append(str(i[5]).strip())
            len0 = len(title)
            text = []
            for i in range(len0):
                dd = {
                'tno': tno[i],
                'title': title[i],
                'label': label[i],
                'date':date[i],
                'cost':cost[i],
                'url':url[i]
            }
                text = text + [dd]
            text={
                'result':'1000',
                'list':text
            }
            return json.dumps(text, ensure_ascii=False)
        except pymssql.IntegrityError:
            flag = '4001'
            text = {
                'result': flag,
                'list':[]
            }
            return json.dumps(text, ensure_ascii=False)

def taskreceived(jwac,tno):#接收任务
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            acceptNum = 3
            sql0 = "select limit from account where jwaccount='%s'" % jwac
            cursor.execute(sql0)
            data = cursor.fetchone()
            if len(data)!=0:
                if data[0]=='2':
                    acceptNum=0
            sql0 = "select count(*) from receivedtask where jwaccount='%s' and static='1'" % jwac
            cursor.execute(sql0)
            data = cursor.fetchone()
            acceptNum0 = int(data[0])
            if acceptNum0 < acceptNum:
                sql = "select jwaccount,title,label,content,accountname,date,cost,num,url from task where tno='%s'" % tno
                cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
                data = cursor.fetchone()
                setjwac = str(data[0]).strip()
                title=str(data[1]).strip()
                label=str(data[2]).strip()
                content=str(data[3]).strip()
                accountname=str(data[4]).strip()
                date=str(data[5]).strip()
                cost=str(data[6]).strip()
                num=str(data[7]).strip()
                url=str(data[8]).strip()
                if setjwac==jwac:
                    flag='4008'
                else:
                    if int(num) >= 1:
                        num = str(int(num) - 1)
                        sql = "update task set num='%s' where tno='%s'" % (num, tno)
                        cursor.execute(sql)
                        conn.commit()

                        it = re.finditer(r"\d+", date)
                        s = ''
                        for match in it:
                            s = s + str(match.group())
                        s = int(s)

                        static='1'
                        sql="insert into receivedtask values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(jwac,tno,title,accountname,content,label,date,cost,setjwac,static,s,url)
                        cursor.execute(sql)
                        conn.commit()
                        flag = '1000'
                    else:
                        flag='4007'
                text = {
                    'result': flag,
                }
                flag = json.dumps(text, ensure_ascii=False)
                return flag
            else:
                flag = '4015'
                text = {
                    'result': flag,
                }
                flag = json.dumps(text, ensure_ascii=False)
                return flag
        except TypeError:
            flag='4002'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
        except pymssql.IntegrityError:
            flag='4001'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag

def searchtask(jwac):#查询进行中的任务订单
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            time0 = int(time.strftime("%m%d%H%M", time.localtime()))
            sql = "update receivedtask set static='0' where time<='%s'" % time0
            cursor.execute(sql)
            conn.commit()
            sql = "select tno,title,label,accountname,date,cost,url from receivedtask where jwaccount='%s' and static='1'" % jwac
            cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
            data = cursor.fetchall()
            tno=[]
            title=[]
            label=[]
            accountname=[]
            date=[]
            cost=[]
            url=[]
            for i in data:
                tno.append(str(i[0].strip()))
                title.append(str(i[1].strip()))
                label.append(str(i[2].strip()))
                accountname.append(str(i[3].strip()))
                date.append(str(i[4].strip()))
                cost.append(str(i[5].strip()))
                url.append(str(i[6].strip()))
            len0 = len(title)
            text = []
            for i in range(len0):
                dd = {
                    'tno': tno[i],
                    'title': title[i],
                    'label': label[i],
                    'accountname':accountname[i],
                    'date': date[i],
                    'cost': cost[i],
                    'url':url[i]
                }
                text = text + [dd]
            text = {
                'result':'1000' ,
                'list': text
            }
            return json.dumps(text, ensure_ascii=False)
        except TypeError:
            flag='4002'
            text = {
                'result': flag,
                'list':[]
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag

def managetask(jwac,tno,type):#对进行中的任务进行操作
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            if type=='finish':
                sql0 = "select jwaccount,tno,title,label,accountname,date,cost,content,setaccount from receivedtask where tno='%s' and jwaccount='%s'" % (tno,jwac)
                cursor.execute(sql0)
                data = cursor.fetchone()
                jwaccount=str(data[0]).strip()
                tno=str(data[1]).strip()
                title = str(data[2]).strip()
                label=str(data[3]).strip()
                accountname=str(data[4]).strip()
                date = str(data[5]).strip()
                cost = str(data[6]).strip()
                content=str(data[7]).strip()
                setaccount=str(data[8]).strip()

                sql = "update receivedtask set static='0' where tno='%s'and jwaccount='%s'" %(tno,jwac)
                cursor.execute(sql)
                conn.commit()
                flag='1000'
                text = {
                    'result': flag,
                }
                flag = json.dumps(text, ensure_ascii=False)
                return flag
            elif type == 'delete':
                sql = "delete from receivedtask where tno='%s' and jwaccount='%s'" % (tno,jwac)
                cursor.execute(sql)
                conn.commit()

                sql0 = "select num from task where tno='%s'" %tno
                cursor.execute(sql0)
                data = cursor.fetchone()
                num = str(data[0]).strip()
                num=str(int(num)+1)
                sql = "update task set num='%s' where tno='%s'" % (num, tno)
                cursor.execute(sql)
                conn.commit()

                flag='1000'
                text = {
                    'result': flag,
                }
                flag = json.dumps(text, ensure_ascii=False)
                return flag

        except TypeError:
            flag = '4002'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
        except pymssql.IntegrityError:
            flag = '4001'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag

def historytask(jwac):#查看接单历史
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            sql = "select tno,title,label,accountname,date,cost,url from receivedtask where jwaccount='%s' and static='0'" % jwac
            cursor.execute(sql)  # 后面不能有conn.commit()，否则提交后无法查询
            data = cursor.fetchall()
            tno=[]
            title=[]
            label=[]
            accountname=[]
            date=[]
            cost=[]
            url=[]
            for i in data:
                tno.append(str(i[0].strip()))
                title.append(str(i[1].strip()))
                label.append(str(i[2].strip()))
                accountname.append(str(i[3].strip()))
                date.append(str(i[4].strip()))
                cost.append(str(i[5].strip()))
                url.append(str(i[6]).strip())
            len0 = len(title)
            text = []
            for i in range(len0):
                dd = {
                    'tno': tno[i],
                    'title': title[i],
                    'label': label[i],
                    'accountname':accountname[i],
                    'date': date[i],
                    'cost': cost[i],
                    'url':url[i]
                }
                text = text + [dd]
            text = {
                'result':'1000' ,
                'list': text
            }
            return json.dumps(text, ensure_ascii=False)
        except TypeError:
            flag='4002'
            text = {
                'result': flag,
                'list':[]
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
def upload_img(url,jwac,type):#图片上传
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            if type=='1':#个人头像上传
                sql = "update data set url='%s' where jwaccount='%s'" % (url,jwac)
                cursor.execute(sql)
                conn.commit()
                sql = "update task set url='%s' where jwaccount='%s'" % (url, jwac)
                cursor.execute(sql)
                conn.commit()
                sql = "update receivedtask set url='%s' where setaccount='%s'" % (url, jwac)
                cursor.execute(sql)
                conn.commit()
            elif type=='2':
                sql = "update data set task_url='%s' where jwaccount='%s'" % (url, jwac)
                cursor.execute(sql)
                conn.commit()
            flag = '1000'
            text = {
                'result': flag,
                'img_url':url
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
        except TypeError:
            flag = '4002'
            text = {
                'result': flag,
                'img_url':''
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag

def searchentry(entry):#搜索框
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            s2 = ['$!', '$!', '$!', '$!', '$!']
            s = '%' + entry + '%'
            sql = "select title,label,accountname,cost,num,tno,date,url from task where (title like '%s' or label like '%s')and num!='0' and static!='0' order by rank*1 desc" % (
            s, s)
            cursor.execute(sql)
            data = cursor.fetchall()
            len0 = len(data)
            if len0 == 0:
                len1 = len(entry)
                if len1 <= 5:
                    for i in range(0, len1):
                        s2[i] = '%' + entry[i] + '%'
                    sql = "select title,label,accountname,cost,num,tno,date,url from task where  (title like '%s' or label like '%s' or title like '%s' or label like '%s'or title like '%s' or label like '%s'or title like '%s' or label like '%s'or title like '%s' or label like '%s')and num!='0' and static!='0' order by rank*1 desc" % (
                    s2[0], s2[0], s2[1], s2[1], s2[2], s2[2], s2[3], s2[3], s2[4], s2[4])
                    cursor.execute(sql)
                    data = cursor.fetchall()
                else:
                    for i in range(0,5):
                        s2[i] = '%' + entry[i] + '%'
                    sql = "select title,label,accountname,cost,num,tno,date,url from task where  (title like '%s' or label like '%s' or title like '%s' or label like '%s'or title like '%s' or label like '%s'or title like '%s' or label like '%s'or title like '%s' or label like '%s')and num!='0' and static!='0' order by rank*1 desc" % (
                        s2[0], s2[0], s2[1], s2[1], s2[2], s2[2], s2[3], s2[3], s2[4], s2[4])
                    cursor.execute(sql)
                    data = cursor.fetchall()
            title = []
            label = []
            account = []
            cost = []
            num = []
            tt = []
            date = []
            url = []
            len0 = len(data)
            for i in data:
                title.append(str(i[0]).strip())
                label.append(str(i[1]).strip())
                account.append(str(i[2]).strip())
                cost.append(str(i[3]).strip())
                num.append(str(i[4]).strip())
                tt.append(str(i[5]).strip())
                date.append(str(i[6]).strip())
                url.append(str(i[7]).strip())
            # print(title, jwac)
            len0 = len(title)
            text = []
            for i in range(len0):
                dd = {
                    'title': title[i],
                    'label': label[i],
                    'accountname': account[i],
                    'cost': cost[i],
                    'num': num[i],
                    'tno': tt[i],
                    'date': date[i],
                    'url': url[i]
                }
                text = text + [dd]
            text = {
                'result': '1000',
                'list': text
            }
            return json.dumps(text, ensure_ascii=False)
        except TypeError:
            flag='4002'
            text = {
                'result': flag,
                'list':[]
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
def intoken(jwac):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            num = 10
            token = ''.join(random.sample(string.ascii_letters + string.digits, num)).join(
                random.sample('$@##$$$^&===============', 10))
            toktime = int((datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime("%m%d%H%M"))#延迟30分钟
            sql = "update account set token='%s' where jwaccount='%s' update account set toktime='%s' where jwaccount='%s'" % (token,jwac,toktime,jwac)
            flag = token
            cursor.execute(sql)
            conn.commit() 
            return flag
        except pymssql.IntegrityError:
            flag = '4001'
            return flag
        except pymssql.OperationalError:  # 数据位溢出
            flag = '4004'
            return flag
def retoken(token):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            sql0 = "select jwaccount from account where token='%s'" % token
            cursor.execute(sql0)
            data = cursor.fetchone()
            if len(data)==0:
                jwac='4002'
            else:
                jwac=data[0]
                print(jwac)
            return jwac
        except pymssql.OperationalError:
            flag='4002'
            return flag
        except TypeError:
            flag='4002'
            return flag
def draw(tno,jwac):
    conn=connect()
    if conn:
        cursor=conn.cursor()
        try:
            if jwac.strip() == '007':
                sql0 = "select setaccount from receivedtask where tno='%s'" % tno
                cursor.execute(sql0)
                data = cursor.fetchone()
                jwac = str(data[0])
            sql0="select jwaccount,static from receivedtask where setaccount='%s' and tno='%s'"%(jwac,tno)
            cursor.execute(sql0)
            data = cursor.fetchall()
            jwac=[]
            static=[]
            for i in data:
                jwac.append(str(i[0]).strip())
                static.append(str(i[1]).strip())
            len1=len(jwac)
            accountname = []
            qq = []
            weixin = []
            tele = []
            url = []
            for i in range(0,len1):
                sql0 = "select accountname,qq,weixin,tele,url from data where jwaccount='%s'" %jwac[i]
                cursor.execute(sql0)
                data = cursor.fetchone()
                accountname.append(str(data[0]).strip())
                qq.append(str(data[1]).strip())
                weixin.append(str(data[2]).strip())
                tele.append(str(data[3]).strip())
                url.append(str(data[4]).strip())
                # print(title, jwac)
            len0 = len(qq)
            text = []
            for i in range(len0):
                dd = {
                    'accountname': accountname[i],
                    'qq': qq[i],
                    'weixin': weixin[i],
                    'tele': tele[i],
                    'url': url[i],
                    'state':static[i],
                }
                text = text + [dd]
            text = {
                'result': '1000',
                'list': text
            }
            return json.dumps(text, ensure_ascii=False)
        except TypeError:
            flag = '4002'
            text = {
                'result': flag,
                'list': []
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
def restatic(token):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            sql0 = "select jwaccount,toktime from account where token='%s'" % token
            cursor.execute(sql0)
            data = cursor.fetchone()
            if len(data)==0:
                flag='4012'#token无效
            else:
                jwac = str(data[0]).strip()
                toktime = str(data[1]).strip()
                if int(toktime)<int(time.strftime("%m%d%H%M", time.localtime())):
                    flag='4013'#token过期
                else:
                    flag='1000'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
        except pymssql.OperationalError:
            flag = '4002'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
def revisepasswd(jwac,passwd,newpasswd):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            sql="select * from account where jwaccount='%s' and passwd='%s'"%(jwac,passwd)
            cursor.execute(sql)
            data = cursor.fetchone()
            if len(data) == 0:
                flag = '4002'
            else:
                sql = "update account set passwd='%s' where jwaccount='%s'" %(newpasswd,jwac)
                cursor.execute(sql)
                conn.commit()
                flag='1000'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag
        except TypeError:
            flag = '4002'
            text = {
                'result': flag,
            }
            flag = json.dumps(text, ensure_ascii=False)
            return flag


if __name__ == '__main__':

    select()
#    dd=zc('sdaskdjsa','sadkajsk','031702228')
#    print(dd)
