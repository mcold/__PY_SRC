from influxdb import InfluxDBClient

json_body = [
                {"measurement": "cpu_load_long2",
                 "fields": {
                                "value": 0.66,
                                "host": 'server01',
                                "region": 'us-west'

                            }
                }
                ]
client = InfluxDBClient('localhost', 8086, 'admin', '15151', 'jmeter')
client.write_points(json_body)
