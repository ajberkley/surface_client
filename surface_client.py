# PYTHON 3.7
import requests
import csv
import json
import argparse
VERSION="0.1 OCTOBER 2019"
AUTHOR="ajberkley@gmail.com"

# URL='http://surface.canadarasp.com:8080/data'
URL='http://localhost:8080/data'

parser = argparse.ArgumentParser(description='For a single longitude and latitude point, generate a CSV file from EC surface archive (%s %s) across a span of time' % (VERSION, AUTHOR))
parser.add_argument('-lon', dest='lon', type=float, help='Longitude of point', required=True)
parser.add_argument('-lat', dest='lat', type=float, help='Latitude of point', required=True)
parser.add_argument('-start', dest='start_time', help='RFC3339 time stamp of starting date/time like 2019-10-01T07:00:00Z', required=True)
parser.add_argument('-end', dest='end_time', help='RFC3339 time stamp of ending date/time like 2019-10-01T08:00:00Z')
parser.add_argument('-var', dest='var', help='sfc_temp, sfc_pres, or wind')
parser.add_argument('-output', help='Output CSV filename')

def get_data_at_point(lon, lat, start_time, var, end_time=None):
    lon_lat_bbox = '%f, %f' % (lon, lat)
    query = {'lon-lat-bbox': lon_lat_bbox, 'start-time': start_time, 'end-time': end_time or start_time, 'var': var}
    r = requests.post(URL, data=query)
    print(r.text)
    return json.loads(r.content)

def write_dicts_to_csv(file, data):
    keys = data[0].keys()
    with open(file,'w') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for datum in data:
            writer.writerow(datum)

args = parser.parse_args()
            
write_dicts_to_csv('blarg.csv',get_data_at_point(args.lon, args.lat, args.start_time, args.var, args.end_time or None))
