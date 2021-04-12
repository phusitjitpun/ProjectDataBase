import psycopg2
from psycopg2 import Error 

try:
    #connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pythonlogin")
    connection = psycopg2.connect(user="webadmin",password="BFCqhr46914", host="node4943-env-2254395.th.app.ruk-com.cloud", port="11043", database="pythonlogin")

    cursor = connection.cursor()

    create_table_guery = '''CREATE TABLE MoneyTHAPI
        (D_M_Y VARCHAR(50) ,
        open_price     VARCHAR(50) ,
        high_price     VARCHAR(50) ,
        low_price     VARCHAR(50) ,
        now_price      VARCHAR(50)); '''

    cursor.execute(create_table_guery)
    connection.commit()
    print("Table created successfully in PostgreSOL ")

except (Exception, psycopg2.DatabaseError) as error: 
    print("Error while creating PostgreSQL table", error) 
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSOL connection is closed")