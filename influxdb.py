from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions



token = "hEypMj9nalLVjF7eyFi40Td2EGsQ6JdpKYR9FnaNiYjuhSmEGYUa6ZNqxI6yADYKmhwvnBFCXF06bhpReqkLSw=="
org = "Danti"
bucket = "data_fetch"
url = "https://eu-central-1-1.aws.cloud2.influxdata.com"  


client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

data_points = [
    {
        "time": "2024-08-16T12:00:00Z",
        "tags": {"location": "xxxx"},
        "fields": {"value": 425.5}
    },
    {
        "time": "2024-08-16T12:00:00Z",
        "tags": {"location": "penarthmandem"},
        "fields": {"value": 4552.5}
    },

      {
        "time": "2024-08-16T12:00:00Z",
        "tags": {"location": "iphone"},
        "fields": {"value": 1000}
    }
]




for data_point in data_points:
    point = Point("measurement_name") \
        .tag("location", data_point["tags"]["location"]) \
        .field("value", data_point["fields"]["value"]) \
        .time(data_point["time"], WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)


write_api.close()
client.close()
