from selenium import webdriver
import pymysql

connent = pymysql.connect(host='localhost', user='root', passwd='hh226752', db='flightradar24', charset='utf8')
cursor = connent.cursor()
browser = webdriver.PhantomJS()

n = 0
ll = []
url = 'https://bj.5i5j.com/zufang/fangshanqu/n{}'
for i in range(1, 43):
    n += 1
    new_url = url.format(i)
    browser.get(new_url)
    # 房名
    Er_name = browser.find_elements_by_css_selector('body > div.pListBox.mar > '
                                                    'div.lfBox.lf > div.list-con-box > ul > li>'
                                                    ' div.listCon > div.listX > p:nth-child(2) > a')
    # 房总价
    Price = browser.find_elements_by_css_selector('body > div.pListBox.mar > div.lfBox.lf > '
                                                  'div.list-con-box > ul > li> div.listCon > '
                                                  'div.listX > div > p.redC > strong')
    # 房单价
    Dan_Price = browser.find_elements_by_css_selector('body > div.pListBox.mar > div.lfBox.lf > '
                                                      'div.list-con-box > ul > li> div.listCon >'
                                                      ' div.listX > div > p:nth-child(2)')
    # 户型面积
    Hu_Xing = browser.find_elements_by_css_selector( 'body > div.pListBox.mar > div.lfBox.lf > '
                                                     'div.list-con-box > ul > li> div.listCon > '
                                                     'div.listX > p:nth-child(1)')

    # 小区名称列表
    Er_name_lis = []
    for m in Er_name:
        Er_name_lis.append(m.text)

    huxing_lis = []  # 小区户型
    mianji_lis = []  # 小区面积
    louceng_lis = []  # 小区楼层
    chaoxiang_lis = []  # 小区朝向
    for k in Hu_Xing:
        try:
            str1 = k.text
            ll = str1.split('·')
            huxing = ll[0]
            mianji = ll[1]
            chaoxiang = ll[2]
            louceng = ll[3]
            huxing_lis.append(huxing)
            mianji_lis.append(mianji)
            chaoxiang_lis.append(chaoxiang)
            louceng_lis.append(louceng)
        except IndexError:
            print('发生错误')

    # 单价列表
    Dan_Price_lis = []
    for j in Dan_Price:
        Dan_Price_lis.append(j.text)

    # 总价列表
    Price_lis = []
    for v in Price:
        Price_lis.append(v.text)

    Mess = zip(Er_name_lis, Price_lis, huxing_lis, mianji_lis, louceng_lis, chaoxiang_lis)
    # print(Mess)
    for j in Mess:
        lis = list(j)
        print(lis)
        lis.insert(0, '房山区')
        sql = "insert into er_shoufang_(Qu,Er_name, Price, Hu_Xing, Mian_Ji, LouCeng, ChaoXiang) values(%s,%s,%s,%s,%s,%s,%s)"
        params = (lis[0], lis[1], lis[2], lis[3], lis[4], lis[5], lis[6])
        cursor.execute(sql, params)
        connent.commit()
    print('-----------房山区----------------：', n)
connent.close()
browser.close()
