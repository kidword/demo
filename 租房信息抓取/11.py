from urllib import parse
import urllib.request
import json
import pymysql as py
query = {
          'key' : 'f247cdb592eb43ebac6ccd27f796e2d2',
          'address':'朝阳区 朝青 华纺易城',
          'output':'json',
           }
base = 'http://api.map.baidu.com/geocoder?'
url = base+parse.urlencode(query)
doc = urllib.request.urlopen(url)
s = doc.read().decode('utf-8')  #一定要解码！！！！
jsonData = json.loads(s)
# lat=jsonData['result']['location']['lat']
# lng =jsonData['result']['location']['lng']
print(jsonData)