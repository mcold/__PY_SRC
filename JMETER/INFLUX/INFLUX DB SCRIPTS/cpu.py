# coding: utf-8

from influxdb import InfluxDBClient
import datetime
import time

cpu_file = 'C:\\Program Files\\GrafanaLabs\\grafana\\data\\CPU_Usage.txt'
json_body = []

with open(cpu_file, 'r') as f:
    l_metrics = f.readlines()
    for l_metr in l_metrics:
        l_metr = l_metr.split(";")
        d_metr = dict()
        d_metr["measurement"] = "cpu"
        d_fields = {"value": int(l_metr[1].strip()), "host": 'server01', "region": 'us-west'}
        d_metr["fields"] = d_fields
        d_metr["time"] = l_metr[0].strip()
        json_body.append(d_metr)


client = InfluxDBClient('localhost', 8086, 'admin', '15151', 'jmeter')
client.write_points(json_body)


