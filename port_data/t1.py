from selenium import webdriver
from lxml import etree
import requests
from user_agents import agents
import random
from lxml import etree

driver = webdriver.Chrome()

# 起始url入口

driver.get("https://www.marinetraffic.com/zh/data/?asset_type=ports&columns=flag,"
            "portname,unlocode,photo,vessels_in_port,vessels_departures,vessels_arrivals,vessels_expected_arrivals,"
            "local_time,anchorage,geographical_area_one,geographical_area_two,coverage")

html = driver.page_source
select = etree.HTML(html)
name = select.xpath("//*[@id='borderLayout_eGridPanel']/div[1]/div/div/div[3]/div[3]/div/div/div/div[2]/div/div/a/@href")
# print(html)
pro = ['http:113.200.56.13:8010', 'http:140.143.105.245:80']

def kangkou():
    url = 'https://www.marinetraffic.com'
    for i in name:
        d = i.replace(" ", "%20")
        urls = url+d
        # print(urls)
        try:
            response = requests.get(url=urls, headers={'User-Agent': random.choice(agents)},
                                    timeout=random.randrange(90, 100))
            html = response.text
            select = etree.HTML(html)
            data = select.xpath('/html/body/main/div/div/div[1]/div[6]/div[1]/div[1]/div[1]/b/text()')
            country = select.xpath('/html/body/main/div/div/div[1]/div[5]/div/div/div[1]/div[2]/span/text()')
            gk = select.xpath("/html/body/main/div/div/div[1]/div[5]/div/div/div[1]/div[1]/h1/text()")
            print(data,country,gk)
        except requests.exceptions.ReadTimeout:
            print('请求超时')
        except requests.exceptions.ConnectionError:
            print('请求错误')
kangkou()
#print(name)
# //*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div[1]/div[2]/div/div
# driver.save_screenshot('weibo.png')
'//*[@id="borderLayout_eGridPanel"]/div[1]/div/div/div[3]/div[3]/div/div/div/div[2]/div/div/a'

'https://www.marinetraffic.com/zh/ais/details/ports/2429/Hong%20Kong_port:HONG%20KONG'