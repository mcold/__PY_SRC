# coding: utf-8

"""
    Work with DBMon plugin result log
"""

from influxdb import InfluxDBClient
import datetime
import time

file = 'DB_LOG.jtl'


def gen():
    """
        Translate 
    """
    json_body = []
    with open(file, 'r') as f:
        l_metrics = f.readlines()
        for i in range(1, len(l_metrics)):
            l_metr = l_metrics[i]
            l_metr = l_metr.split(",")
            d_metr = dict()
            d_metr["measurement"] = l_metr[2]
            d_fields = {"value": int(float(l_metr[4].strip()))}
            d_metr["fields"] = d_fields
            # minus 3 hour - cause UTC
            d_metr["time"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(int(l_metr[0][:-3].strip()) - 10800))
            
            json_body.append(d_metr)

    client = InfluxDBClient('localhost', 8086, 'admin', '15151', 'jmeter')
    client.write_points(json_body)


if __name__ == "__main__":
    gen()