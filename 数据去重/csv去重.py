import pandas as pd
# 将new_flight 数据删除不需要列
# 合并两个list 然后读取csv文件数据，转化成list，在对数据进行去重操作，保存到csv文件
read = pd.read_csv(r'D:/new_flight.csv')

def read_csv(file_name):
    f = open(file_name, 'r',encoding = 'utf-8')
    content = f.read()
    final_list = list()
    rows = content.split('\n')
    for row in rows:
        final_list.append(row.split(','))
    return final_list
list = read_csv(r'D:/new_flight.csv')
new_lis = list[1:-2]
shuju = []
for i in new_lis:
    lis = i[3:]
    shuju.append(lis)


print(shuju[0])
name = ['Take_off_airport_country','Take_off_airport_name','Take_off_airport_code','Take_off_airport_alt','Take_off_airport_lon','Landing_airport_country','Landing_airport_name','Landing_airport_code','Landing_airport_city','Landing_lat','Landing_lon','ID']
test = pd.DataFrame(columns=name,data=shuju)
test.to_csv(r"D:\新航班数据.csv")
#read.drop_duplicates(subset =['列名1'，'列名2']，keep = 'first')
# 58679
# 112311


