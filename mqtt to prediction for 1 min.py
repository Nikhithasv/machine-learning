 code for prediction for one minute:
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
while True:
        
    cnx = mysql.connector.connect(user='root', password='',host='localhost', database='demo')

# Create a cursor object
    cursor = cnx.cursor()
    sql = "SELECT * FROM db ORDER BY no ASC"
    cursor.execute(sql)
    rows = cursor.fetchall()
    data=pd.DataFrame(rows,columns=['no','rv','yv','bv','Av','ri','yi','bi','avi','avp','time_base'])
    print(data)
    data['time_base']=pd.to_datetime(data['time_base'])
    a=pd.to_datetime(data['time_base'])
    print(a)
    data.set_index(['time_base'], inplace=True)

# Apply exponential smoothing to the 'rno' values
    avp_intensity = data['bv']
    avp_intensity_smoothed = avp_intensity.ewm(alpha=0.2).mean()
    mse = mean_squared_error(avp_intensity, avp_intensity_smoothed)
    X = avp_intensity_smoothed.values.reshape(-1, 1)
    y = avp_intensity.values.reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Predicted values:", y_pred)
    last_timestamp = data.index[-1]




   
# Predict the gas value after one minute
    next_timestamp = last_timestamp + pd.DateOffset(minutes=1)
    prediction = avp_intensity.loc[last_timestamp]


    print(type(next_timestamp))
    print(next_timestamp)

    print('Exponential Smoothing Results:')
    print('-------------------------------')
 #print('Accuracy: {:.2f}%'.format(accuracy * 100))
    print('Prediction for {}: {}'.format(next_timestamp, prediction))
    def get_current_timestamp():
      return datetime.datetime.now()
    plt.figure(figsize=(10, 6))
    plt.plot(avp_intensity.index, avp_intensity, label='Original')
    plt.plot(avp_intensity_smoothed.index, avp_intensity_smoothed, label='Smoothed')
    plt.xlabel('Time')
    plt.ylabel('b phase voltage)
    plt.legend()
    plt.show()


