import mysql.connector
import paho.mqtt.client as mqttClient
from threading import Thread
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import mysql.connector
import datetime
import calendar
import time


class Mqtt:
    def __init__(self):
        self.json_data = {}
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            db="demo")
        mqttclient = mqttClient.Client("52244535477668454")
        mqttclient.on_connect = self.on_connect
        mqttclient.on_message = self.on_message
        #print(mqttclient.on_message)
        mqttclient.username_pw_set(username="",password="")
        mqttstatus = mqttclient.connect("broker.emqx.io", 1883,60)
        mqttclient.subscribe("/meter/data",2)
        mqttclient.loop_forever()


    def upload(self,msg):
        mqtt_msg = str(msg.payload).replace("b'", "").replace("'", "").replace("  ", "").replace("\\n", "").replace("\n", '')
        print(msg.payload)
        mqtt_msg = str(mqtt_msg).replace("\\","")
        mqtt_msg = str(mqtt_msg).replace('}"','}')
        mqtt_msg = str(mqtt_msg).replace('"{','{')
        mqtt_msg = str(mqtt_msg).replace('{','')
        mqtt_msg = str(mqtt_msg).replace('}','')
        mqtt_msg = str(mqtt_msg).replace('"','')
        mqtt_msg = mqtt_msg.split(",")
        #print("====",mqtt_msg)
        #print("=----",mqtt_msg[2])
       
        rv = mqtt_msg[2].split(":")[1]
        print("rv:"+rv+"end")
        #ya = mqtt_msg[4].split(":")[1]
        #ba = mqtt_msg[5].split(":")[1]
        #rv = mqtt_msg[1].split(":")[1]
        #print("rv:"+rv+"end")
        yv = mqtt_msg[5].split(":")[1]
        print("yv:"+yv+"end")
        bv = mqtt_msg[8].split(":")[1]
        print("bv:"+bv+"end")
        Av = mqtt_msg[11].split(":")[1]
        print("Av:"+Av+"end")
        ri = mqtt_msg[14].split(":")[1]
        print("ri:"+ri+"end")
        yi = mqtt_msg[17].split(":")[1]
        print("yi:"+yi+"end")
        bi = mqtt_msg[20].split(":")[1]
        print("bi:"+bi+"end")
        avi = mqtt_msg[23].split(":")[1]
        print("avi:"+avi+"end")
        rpf = mqtt_msg[26].split(":")[1]
        print("rpf:"+rpf+"end")
        ypf = mqtt_msg[29].split(":")[1]
        print("ypf:"+ypf+"end")
        bpf = mqtt_msg[32].split(":")[1]
        print("bpf:"+bpf+"end")
        avp = mqtt_msg[35].split(":")[1]
        print("avp:"+avp+"end")
        energy = mqtt_msg[3].split(":")[1]
       
        mycursor = self.db.cursor()
        sql = 'INSERT INTO db (rv,yv,bv,Av,ri,yi,bi,avi,avp) VALUES ('+rv+','+yv+','+bv+','+Av+','+ri+','+yi+','+bi+','+avi+','+avp+')'
        mycursor.execute(sql)
        self.db.commit()
        #print(ra)
        print(rv)
        print(yv)
        print(bv)
        print("Data Inserted!")
        cnx = mysql.connector.connect(user='root', password='',host='localhost', database='demo')

# Create a cursor object
        cursor = cnx.cursor()
        sql = "SELECT * FROM db ORDER BY no ASC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        data=pd.DataFrame(rows,columns=['no','rv','yv','bv','Av','ri','yi','bi','avi','avp','time_base'])
        print(data)
    def on_connect(self,mqttclient, userdata, flags,rc):
        if rc == 0:
            print("connected!")
        else:
            print("Connection failed")


    def on_message(self, mqttclient, userdata, msg):
        Thread(target=self.upload, args=(msg,)).start()
       # print("enter")


if __name__ == '__main__':
    Mqtt()
