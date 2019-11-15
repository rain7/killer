from bs4 import BeautifulSoup
import requests
import  re
import requests
def jw(user,passwd):
    url='http://59.77.226.32/logincheck.asp'
    headers={
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Referer': 'http://jwch.fzu.edu.cn/'
    }
    data={
        'muser': user,
        'passwd': passwd,
        'x':'40',
        'y':'34'
    }
    wbdata = requests.post(url, data=data,headers=headers).text
    soup = BeautifulSoup(wbdata, 'lxml')
    #print(soup)
    soup=str(soup)
    if re.search('福州大学教务处本科教学管理系统',soup)!=None:
        print('教务处认证成功')
        flag='1000'
    else:
        print('账号或密码错误')
        flag='4001'
    return flag