from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
import os
import csv
from datetime import datetime, timedelta



token = "8luTGcM4rMkDcTH6KuQG2oXnUdsFYnOHcU-kvPNSGUvhK54AQ2Wo5TeHObFuNLRIVxBODau0PcMgsS6K2nDMWg=="
org = "Danti"
bucket = "trading"
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"  


client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))



directory = "/Users/vincentsalter/Documents/GitHub/Data_Fetch/src/data"

time_offset = timedelta(365)
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
            
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
                
            for row in csv_reader:
                buy_date = datetime.strptime(row["Buy Date"], "%Y-%m-%d") + time_offset
                sell_date = datetime.strptime(row["Sell Date"], "%Y-%m-%d") + time_offset
                
                # Create a point for each row in the CSV
                point = Point("trades") \
                    .field("Buy Price", float(row["Buy Price"])) \
                    .field("Sell Price", float(row["Sell Price"])) \
                    .field("Long Profit", float(row["Long Profit"])) \
                    .tag("Buy Date", buy_date)\
                    .tag("Sell Date", sell_date)
                
                write_api.write(bucket=bucket, org=org, record=point)


write_api.close()
client.close()
