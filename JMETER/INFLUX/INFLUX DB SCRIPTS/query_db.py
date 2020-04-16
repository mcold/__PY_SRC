# coding: utf-8

from influxdb import InfluxDBClient

client = InfluxDBClient(host='127.0.0.1', port=8086, username='admin', password='15151', database='jmeter')


qs = client.query('SELECT "duration" FROM "jmeter"."autogen"."brushEvents" WHERE time > now() - 4d GROUP BY "user"')

qs = client.query('SELECT "duration" FROM "jmeter"."autogen"."all.a.max" WHERE time > now() - 4d GROUP BY "user"')