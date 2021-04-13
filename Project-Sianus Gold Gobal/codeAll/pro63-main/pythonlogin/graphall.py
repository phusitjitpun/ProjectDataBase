import psycopg2
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
connection = psycopg2.connect(user="webadmin",
                                password="BFCqhr46914", 
                                host="node4943-env-2254395.th.app.ruk-com.cloud", 
                                port="11043", 
                                database="pythonlogin")
cursor = connection.cursor()
cursor.execute('SELECT * FROM MoneyTHAPI')
money_records = cursor.fetchall()
date=[]
price=[]
for i in money_records:
    date.append((i[0])[0:2])
    a = float(i[-1])
    price.append(a)
tick_label = date
plt.plot(date,price,color='red')
plt.title('SilverBath')
plt.xlabel('Date')
plt.ylabel('Rate')
plt.savefig('pythonlogin/static/images/mymoney03.png')
plt.close()
cursor.close()
cursor = connection.cursor()
cursor.execute('SELECT * FROM GoldAPI')
Goldapi_records = cursor.fetchall()
date=[]
tict=[]
for y in Goldapi_records:
    date.append((y[0])[0:2])
    c = float(y[3])
    tict.append(c)
tick_label = date 
plt.plot(date,tict,color='blue')
plt.title('Gold Global')
plt.xlabel('Date')
plt.ylabel('Rate')
plt.savefig('pythonlogin/static/images/goldapiplot3.png')
plt.close()
cursor.close()
cursor = connection.cursor()
cursor.execute('SELECT * FROM GoldTH')
Goldth_records = cursor.fetchall()
date=[]
tict=[]
for y in Goldth_records:
    date.append((y[0])[0:2])
    x = str(y[3])
    q = x.split(",")
    p = q[0]+q[1]
    c = float(p)
    tict.append(c)
plt.plot(date,tict,color='g')
plt.title('GoldTH')
plt.xlabel('Date')
plt.ylabel('Rate')
plt.savefig('pythonlogin/static/images/goldthplot3.png')
cursor.close()
connection.close()
