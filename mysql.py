import pymssql
import json
import time
def connect():
    flag = pymssql.connect(host='localhost', server='LAPTOP-14UCF6FH\SQL2012', port='51430', user='sa', password='123456',
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

def zc(user,password,jwaccount):
    conn=connect()
    if conn:
        cursor = conn.cursor()  # 创建游标对象
        try:
            sql = "insert into account values('%s','%s','%s')  insert into data values('','','','','%s')"%(user,password,jwaccount,jwaccount)
            flag='1000'
            cursor.execute(sql)
            conn.commit()  # 提交修改，不然数据库上不会更新
        except pymssql.IntegrityError:
            flag='4001'

        cursor.close()  # 关闭游标
        conn.close()
    else:
        flag='2001'
    return flag
def relogin(user,password):
    conn = connect()
    if conn:
        cursor = conn.cursor()  # 创建游标对象
        sql = 'select username,passwd,jwaccount from account'
        cursor.execute(sql)
        data = cursor.fetchall()
        username = []
        passwd=[]
        jwaccount=[]
        for i in data:
            username.append( str(i[0]).strip())
            passwd.append(str(i[1]).strip())
            jwaccount.append(str(i[2]).strip())
        return username,passwd,jwaccount

def redata(accountname,room,qq,weixin,jwac):
    conn=connect()
    if conn:
        try:
            cursor=conn.cursor()
            sql="update data set accountname='%s',room='%s',qq='%s',weixin='%s' where jwaccount='%s'"%(accountname,room,qq,weixin,jwac)
            cursor.execute(sql)
            conn.commit()
            flag='1000'
        except pymssql.IntegrityError:
            flag = '4001'
    else:
        flag='2001'
    return flag

def finddata(jwac):
    conn=connect()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "select accountname,room,qq,weixin from data where jwaccount='%s'"%jwac
            cursor.execute(sql)
            data = cursor.fetchone()
            text={
                'accountname': str(data[0]).strip(),
                'room':str(data[1]).strip(),
                'qq':str(data[2]).strip(),
                'weixin':str(data[3]).strip()
            }

            return json.dumps(text, ensure_ascii=False, indent=4)
        except pymssql.IntegrityError:
            pass

def forget(user,jwac):
    conn=connect()
    if conn:
        try:
            cursor=conn.cursor()
            sql="select passwd from account where jwaccount='%s' and username='%s'"%(jwac,user)
            cursor.execute(sql)
            data=cursor.fetchone()
            passwd=str(data[0]).strip()
            return passwd
        except pymssql.IntegrityError:
            flag='4001'
            return flag
def puttask(jwac,tno,title,label,content,method):
    conn=connect()
    if conn:
        try:
            cursor=conn.cursor()
            if method=='insert':
                tno=time.strftime("%H%M%S", time.localtime())#任务号生成
                sql="insert into task values('%s','%s','%s','%s','%s','%s')"%(jwac,tno,title,label,content)
                cursor.execute(sql)
                conn.commit()
            elif method=='updata':
                sql="updata task set content='%s' where jwaccount='%s' and tno='%s'"%(content,jwac,tno)
                cursor.execute(sql)
                conn.commit()
            elif method=='delect':
                sql="delect from task where jwaccount='%s' and tno='%s'"
                cursor.execute(sql)
                conn.commit()




if __name__ == '__main__':

    select()
    zc('rain88','123456')