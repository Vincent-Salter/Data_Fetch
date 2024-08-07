from influxdb_client import InfluxDBClient, Point, WritePrecision

# Define your InfluxDB connection parameters
token = "your_influxdb_token"
org = "your_organization"
bucket = "your_bucket"
url = "http://localhost:8086"  # Change to your InfluxDB instance URL

# Initialize the InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

# Example data to write
data_points = [
    {"measurement": "temperature", "tags": {"location": "room1"}, "fields": {"value": 23.5}, "time": "2024-08-04T00:00:00Z"},
    {"measurement": "temperature", "tags": {"location": "room2"}, "fields": {"value": 22.1}, "time": "2024-08-04T01:00:00Z"},
    {"measurement": "humidity", "tags": {"location": "room1"}, "fields": {"value": 45.0}, "time": "2024-08-04T00:00:00Z"},
    {"measurement": "humidity", "tags": {"location": "room2"}, "fields": {"value": 50.0}, "time": "2024-08-04T01:00:00Z"}
]

# Write data points to InfluxDB using a for loop
for data_point in data_points:
    point = Point(data_point["measurement"]) \
        .tag("location", data_point["tags"]["location"]) \
        .field("value", data_point["fields"]["value"]) \
        .time(data_point["time"], WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)

# Close the client
client.close()
