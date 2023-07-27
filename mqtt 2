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

#current_timestamp = datetime.datetime.now()
#while True:
# Connect to the MySQL database
cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='demo')
#dt,sub,temp,pre,flow,mac
# Create a cursor object
cursor = cnx.cursor()

# Retrieve the latest row from the 'number' table
sql = "SELECT * FROM sensors ORDER BY sno ASC"
cursor.execute(sql)
rows = cursor.fetchall()
data = pd.DataFrame(rows, columns=['sno', 'dt','sub','temp','pre','flow','mac'])
print(data)
cnx.commit()
cnx.close()
s=data['sub']
t=data['temp']
p=data['pre']
f=data['flow']
m=data['mac']

sub=s
temp=t
pre=p
flow=t
mac=m
data['dt'] = pd.to_datetime(data['dt'])

# Set the 'actual_time' column as the index
data.set_index(['dt'], inplace=True)

# Apply exponential smoothing to the 'temp' values
temp_intensity = data['temp']
temp_intensity_smoothed = temp_intensity.ewm(alpha=0.2).mean()
mse = mean_squared_error(temp_intensity, temp_intensity_smoothed)
X = temp_intensity_smoothed.values.reshape(-1, 1)
y = temp_intensity.values.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Predicted values:", y_pred)
last_timestamp = data.index[-1]
next_timestamp = last_timestamp + pd.DateOffset(minutes=1)
prediction = temp_intensity.loc[last_timestamp]


print(type(next_timestamp))
print(next_timestamp)

print('Exponential Smoothing Results:')
print('-------------------------------')
#print('Accuracy: {:.2f}%'.format(accuracy * 100))
print('Prediction for {}: {}'.format(next_timestamp, prediction))

plt.figure(figsize=(10, 6))
plt.plot(temp_intensity.index, temp_intensity, label='Original')
plt.plot(temp_intensity_smoothed.index, temp_intensity_smoothed, label='Smoothed')
plt.xlabel('Time')
plt.ylabel('temp')
plt.legend()
plt.show()
mydb = mysql.connector.connect(host="localhost",user="root",password="",database="prediction")
myser = mydb.cursor()

predict_int = prediction.item()
predict_epoch = calendar.timegm(next_timestamp.timetuple())
epoch_date_time = datetime.datetime.fromtimestamp(predict_epoch)

def get_current_timestamp():
    return datetime.datetime.now()
ct=get_current_timestamp()
def iso_to_utc(epoch_date_time):
    # Convert the iso_time string to a datetime object
 dt = datetime.datetime.fromisoformat(str(epoch_date_time))
   
    # Convert the datetime object to UTC time
 utc_time = dt.astimezone(datetime.timezone.utc)
   
 return utc_time

# Example usage
iso_time = epoch_date_time
utc_time = iso_to_utc(iso_time)
print(utc_time)
print(type(predict_int))
print(type(epoch_date_time),epoch_date_time)
print(type(next_timestamp),next_timestamp)
a=iso_to_utc(epoch_date_time)
print(a)
sql = 'INSERT INTO `livepred`(dt,sub,temp,pre,flow,mac) VALUES (%s,%s,%s,%s,%s,%s)'

myser.execute(sql, (a,sub,predict_int,pre,flow,mac))
 
 
mydb.commit()
print("Insertion success")
   

        # Generate a timestamp
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Current timestamp:", current_time)

        # Sleep for one minute
time.sleep(10)  # Sleep for 1 minute

# Close the cursor and the database connection
myser.close()
  #cnx.close()
