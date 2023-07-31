
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

current_timestamp = datetime.datetime.now()
while True:
# Connect to the MySQL database
 cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='prediction')

# Create a cursor object
 cursor = cnx.cursor()

# Retrieve the latest row from the 'number' table
 sql = "SELECT * FROM number ORDER BY id ASC"
 cursor.execute(sql)
 rows = cursor.fetchall()
 data = pd.DataFrame(rows, columns=['id', 'actual_time','rno'])
 print(data)



# Convert the 'actual_time' column to datetime
 data['actual_time'] = pd.to_datetime(data['actual_time'])

# Set the 'actual_time' column as the index
 data.set_index(['actual_time'], inplace=True)

# Apply exponential smoothing to the 'rno' values
 smoke_intensity = data['rno']
 smoke_intensity_smoothed = smoke_intensity.ewm(alpha=0.2).mean()
 mse = mean_squared_error(smoke_intensity, smoke_intensity_smoothed)
 X = smoke_intensity_smoothed.values.reshape(-1, 1)
 y = smoke_intensity.values.reshape(-1, 1)
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 model = LinearRegression()
 model.fit(X_train, y_train)
 y_pred = model.predict(X_test)
 print("Predicted values:", y_pred)
 last_timestamp = data.index[-1]




   
# Predict the gas value after one minute
 next_timestamp = last_timestamp + pd.DateOffset(minutes=1)
 prediction = smoke_intensity.loc[last_timestamp]


 print(type(next_timestamp))
 print(next_timestamp)

 print('Exponential Smoothing Results:')
 print('-------------------------------')
 #print('Accuracy: {:.2f}%'.format(accuracy * 100))
 print('Prediction for {}: {}'.format(next_timestamp, prediction))
 def get_current_timestamp():
   return datetime.datetime.now()
#plt.figure(figsize=(10, 6))
#plt.plot(smoke_intensity.index, smoke_intensity, label='Original')
##plt.plot(smoke_intensity_smoothed.index, smoke_intensity_smoothed, label='Smoothed')
#plt.xlabel('Time')
#plt.ylabel('gasData')
#plt.legend()
#plt.show()



 mydb = mysql.connector.connect(host="localhost",user="root",password="",database="prediction")
 myser = mydb.cursor()
 create_table_query = """
        CREATE TABLE IF NOT EXISTS predictions (
            rno INT AUTO_INCREMENT PRIMARY KEY,
            actual_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            predict_value INT,
            predict_time DATETIME
         
        )
    """
 myser.execute(create_table_query)

 predict_int = prediction.item()
 predict_epoch = calendar.timegm(next_timestamp.timetuple())
 epoch_date_time = datetime.datetime.fromtimestamp(predict_epoch)
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
 sql ="INSERT INTO predictions (actual_time, predict_value,predict_time) VALUES (%s, %s,%s)"
 myser.execute(sql, (ct,predict_int,a))
 
 sq ="INSERT INTO number (actual_time,actual_value) VALUES (%s,%s)"
 myser.execute(sq, (ct,predict_int))
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
# Plot the original and smoothed smoke intensity values
plt.figure(figsize=(10, 6))
plt.plot(smoke_intensity.index, smoke_intensity, label='Original')
plt.plot(smoke_intensity_smoothed.index, smoke_intensity_smoothed, label='Smoothed')
plt.xlabel('Time')
plt.ylabel('gasData')
plt.legend()
plt.show()
