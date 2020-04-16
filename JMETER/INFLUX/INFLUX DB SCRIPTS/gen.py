# coding: utf-8

from influxdb import InfluxDBClient

client = InfluxDBClient(host='127.0.0.1', port=8086, username='admin', password='15151', database='jmeter')

json_body = [
    {
        "measurement": "brushEvents2",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2020-04-04T17:29:00Z",
        "fields": {
            "duration": 127
        }
    },
    {
        "measurement": "brushEvents2",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2020-04-04T17:29:00Z",
        "fields": {
            "duration": 132
        }
    },
    {
        "measurement": "brushEvents2",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2020-04-04T17:29:00Z",
        "fields": {
            "duration": 129
        }
    }
]

client.write_points(json_body)