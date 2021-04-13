import requests  
from bs4 import BeautifulSoup
from datetime import date
import datetime
import time
import http.client
import psycopg2
while True:
    nowdate = datetime.datetime.now()
    nowdate = nowdate.strftime("%H/%M/%S")
    nowdate = str(nowdate)
    if nowdate =="23/10/00":#<<<<run code ทิ้งไว้จะทำงานเองตามเวลา
        page = requests.get("https://xn--42cah7d0cxcvbbb9x.com/%E0%B8%84%E0%B9%88%E0%B8%B2%E0%B9%80%E0%B8%87%E0%B8%B4%E0%B8%99%E0%B8%9A%E0%B8%B2%E0%B8%97-%E0%B8%AA%E0%B8%A3%E0%B8%B8%E0%B8%9B%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%84%E0%B8%A5%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%99%E0%B9%84%E0%B8%AB%E0%B8%A7%E0%B9%80%E0%B8%87%E0%B8%B4%E0%B8%99%E0%B8%9A%E0%B8%B2%E0%B8%97%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%88%E0%B8%B3%E0%B8%A7%E0%B8%B1%E0%B8%99-%E0%B8%A2%E0%B9%89%E0%B8%AD%E0%B8%99%E0%B8%AB%E0%B8%A5%E0%B8%B1%E0%B8%87/") 
        soup = BeautifulSoup(page.content, 'html.parser')
        data_list = soup.find_all("td")
        count = -1
        open_price =""
        now_price =""
        top_price =""
        datemoney =""
        low_price =""
        for i in data_list[0:5]:
            count += 1
            i = str(i)
            if count == 0:
                datemoney += i[4:-5]
                datemoney = datemoney.split(" ")
            elif count == 1:
                now_price += i[15:21]
            elif count == 2:
                open_price += i[4:10]
            elif count == 3:
                top_price += i[4:10]
            elif count == 4:
                low_price += i[4:10]
        page = requests.get("https://xn--42cah7d0cxcvbbb9x.com/") 
        soup = BeautifulSoup(page.content, 'html.parser')
        data_list = soup.find_all("td",class_="em bg-em g-u")
        if data_list == []:
            data_list = soup.find_all("td",class_="em bg-em g-d")
        hardsell = ""
        hardbuy = ""
        picsell = ""
        picbuy = ""
        count = -1
        data2 = soup.find_all('td',class_="span bg-span txtd al-r")
        dategold =""
        data2 = str(data2)
        dategold += data2[36:-5]
        dategold = dategold.split(" ")
        for i in data_list:
            count += 1
            i = str(i)
            if count == 0:
                hardbuy += i[25:-5]
            elif count == 1:
                hardsell += i[25:-5]
            elif count == 2:
                picbuy += i[25:-5]
            elif count ==3:
                picsell += i[25:-5]
        conn = http.client.HTTPSConnection("www.goldapi.io")
        payload = ''
        headers = {
                'x-access-token': 'goldapi-3o2nyukgc3rzcm-io',
                'Content-Type': 'application/json'
        }
        conn.request("GET", "/api/XAU/USD", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data.decode("utf-8")
        a = data.decode("utf-8")
        a = a.split(",")
        lowprice = (a[7])[12:]
        highprice = (a[8])[13:]
        price = (a[10])[8:]
        today = date.today()
        DD = today.strftime("%d/%m/%y")
        nowDD = str(DD)
        datetest = nowDD.split(nowDD[0:2])
        nowmoneydate = datemoney[1]+datetest[1]
        newdategold = dategold[0]+datetest[1]
        #connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pythonlogin")
        connection = psycopg2.connect(user="webadmin",password="BFCqhr46914", host="node4943-env-2254395.th.app.ruk-com.cloud", port="11043", database="pythonlogin")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM MoneyTHAPI')
        money_records = cursor.fetchall()
        if (money_records[-1])[0] == nowmoneydate:
            pass
        else:
            postgres_insert_query = """ INSERT INTO MoneyTHAPI (D_M_Y,open_price, high_price, low_price,now_price) VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(postgres_insert_query,(nowmoneydate,open_price,top_price,low_price,now_price))
            connection.commit()
        cursor.execute('SELECT * FROM GoldTH')
        goldth_records = cursor.fetchall()
        if (goldth_records[-1])[0] == newdategold:
            pass
        else: 
            postgres_insert_query = """ INSERT INTO GoldTH (D_M_Y,hard_buy, hard_sell, pic_buy,pic_sell) VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(postgres_insert_query,(newdategold,hardbuy,hardsell,picbuy,picsell))
            connection.commit()
        postgres_insert_query = """ INSERT INTO GoldAPI (D_M_Y, low_price, high_price,price_USD) VALUES (%s,%s,%s,%s)"""
        cursor.execute(postgres_insert_query,(nowDD,lowprice,highprice,price))
        connection.commit()
        cursor.close()
        connection.close()
        time.sleep(10)
            