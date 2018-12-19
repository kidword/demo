import requests
import threading
from bs4 import BeautifulSoup

import random
import pymysql as py


headers = ['Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
           'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
           "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
           "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
           ]


def lianjie():
    conn = py.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
    return conn
conn = lianjie()

def parse(url,qu):
    # 必须要通过解析得到页码数
    global name,huxing,mianji,chaoxiang,price,data,area,louceng,page,result
    new = url+str(1)
    htm = requests.get(url, headers={'User-Agent': random.choice(headers)})
    soup = BeautifulSoup(htm.text, 'lxml')
    try:
        next = soup.find('div',attrs={'class':'page-box house-lst-page-box'}).get('page-data')
        data = eval(next)['totalPage']
        page = int(data)
    except:
        print('未解析出page页码数')
    for u in range(1,page+1):
        urls = url+str(u)
        req = requests.get(url = urls,headers={'User-Agent':random.choice(headers)})
        html = BeautifulSoup(req.text, 'lxml')
        try:
                result = html.select('div[class="info-panel"]')
        except:
            print('未解析出对应div')
        for site in result:
            try:
                name = site.select('span')[0].get_text() #名称
                area = site.select('.con a')[0].get_text()
                louceng = site.select('.con span')[0].next_sibling
                huxing = site.select('span')[1].get_text()  # 户型
                mianji = site.select('.meters')[0].get_text() # 面积
                chaoxiang = site.select('span')[4].get_text() # 朝向
                price = site.select('.price span')[0].get_text() # 价格
                data = site.select('.price-pre')[0].get_text() # 发布时间
                print(name,area,louceng, huxing, mianji,chaoxiang,price,data)
            except:
                print('未解析出对应div下面元素')
            try:
                con = conn.cursor()
                sql = "insert into zufang_copy_copy(qu,name,area,louceng,price) values(%s,%s,%s,%s,%s)"
                params = (qu,name,area,louceng,price)
                # con.execute(sql, params)
                # conn.commit()
            except Exception:
                print('数据库连接错误，请检查数据......')



# 创建新线程
thread1 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/dongcheng/pg','东城区'))
thread2 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/xicheng/pg','西城区'))
thread3 = threading.Thread(target=parse,args=( 'https://bj.lianjia.com/ershoufang/chaoyang/pg','朝阳区'))
thread4 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/haidian/pg','海淀区'))
thread5 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/fengtai/pg','丰台区'))
thread6 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/shijingshan/pg','石景山区'))
thread7 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/tongzhou/pg','通州区'))
thread8 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/changping/pg','昌平区'))
thread9 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/daxing/pg','大兴区'))
thread10 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/shunyi/pg','顺义区'))
thread11 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/tongzhou/pg','房山区'))
thread12 = threading.Thread(target=parse,args=('https://bj.lianjia.com/ershoufang/yanjiao/pg','燕郊'))


# 数据去重
def data():
    try:
        con = conn.cursor()
        sql = ""
        con.execute(sql)
        conn.commit()
    except:
        print('sql语句发生错误')
# 开启线程
if __name__ == '__main__':
    threads = [thread1,thread2,thread3,thread4,thread5,thread6,thread7,thread8,thread9,thread10,thread11,thread12]
    for t in threads:
        t.start()
        t.join()
    #data()
    # 关闭数据库连接
    conn.close()





