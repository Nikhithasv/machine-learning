import random
import mysql.connector
import datetime
import time

def get_current_time():
    return datetime.datetime.now()
a=str(datetime.datetime.now())


def my_function(value):
  mydb = mysql.connector.connect(host="localhost",user="root",password="",database="prediction")

  myser = mydb.cursor()
  #sql = "INSERT INTO accelerometers(avalues) VALUES("+str(random_number)+")"
  #sql = "INSERT INTO image(ivalue) VALUES("+str(random_number)+")"
  #sql = "INSERT INTO infrared(irvalues) VALUES("+str(random_number)+")"
 # sql = "INSERT INTO level(lvalues) VALUES("+str(random_number)+")"
  #sql = "INSERT INTO motion(mvalues) VALUES("+str(random_number)+")"
  #sql = "INSERT INTO pressure(pvalues) VALUES("+str(random_number)+")"
  sql = "INSERT INTO number(actual_time,actual_value) VALUES("+a+","+str(random_number)+")"
 
  myser.execute(sql)
  mydb.commit()
while True:
    random_number = random.randint(100,500)
    print("Random number:", random_number)
   
    my_function(random_number)
