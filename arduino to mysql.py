python code to insert into database:
import serial
import mysql.connector

def insert_data(mydata):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mq2new"
        )
    my_arr = mydata.split(',')
    mycursor = mydb.cursor()
    sql='INSERT INTO mq2(gas) VALUES ('+my_arr[0]+')'
    mycursor.execute(sql)
    mydb.commit()
    print("insertion success")

while True:
    
    myser = serial.Serial("COM12" ,9600,
                          parity=serial.PARITY_NONE,
                          stopbits=serial.STOPBITS_ONE,
                          bytesize=serial.EIGHTBITS)
   
    line  = (myser.readline())
   
    data = line.decode('utf-8')
    print(data)
  

    insert_data(data)
    myser.close()

