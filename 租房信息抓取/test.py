# 读取数据库qu和name字段去网页上搜索坐标信息放到数据库中
import pymysql as py
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import threading

driver = webdriver.PhantomJS()


def getmysql():
    return py.connect(host='localhost', user='root', password='hh226752', db='flightradar24', charset='utf8')

conn = getmysql()
cur = conn.cursor()
cn = cur.execute('select qu,name from zufang_copy')
rows = cur.fetchall()
rows = list(rows)
print(rows)

list_info = []


def getarea():
    global soup
    driver.get('http://api.map.baidu.com/lbsapi/getpoint/index.html')
    for name in rows:
        names = str(name[0])+str(name[1])
        driver.find_element_by_id('localvalue').send_keys(names)
        driver.find_element_by_class_name('button').click()
        # 点击完成必须休眠
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        reslt = soup.select('#no_0 p')
        for area in reslt:
            areas = area.select('br')[0].next_sibling
            print(areas)
            try:
                ar = areas[3:].split(',')
                list_info.append(ar[0])
            except:
                ss = area.select('br')[1].next_sibling
                list_info.append(ss)
        driver.find_element_by_id('localvalue').clear()


def Intomysql():
    con = conn.cursor()
    sql = "insert into er_shoufang_copy(lat,lon) values(%s,%s)"
    params = (list_info[0],list_info[1])
    con.execute(sql, params)
    conn.commit()

# 去掉那些错误数据
# def quchu():
#     qu_conn = getmysql()
#     qu_cur = qu_conn.cursor()
#     cn = cur.execute('select qu,name from zufang')

if __name__ == '__main__':
    Thread1 = threading.Thread(target=getarea)
    Thread2 = threading.Thread(target=Intomysql)
    threads = [Thread1, Thread2]
    for i in threads:
        i.start()
        i.join()
    driver.quit()

