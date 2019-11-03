# PYTHON 3.7
import iso8601
import requests
import csv
import json
import argparse
import sys
import tzlocal
VERSION="v0.3 November 2019"
AUTHOR="ajberkley@gmail.com"

PROG_DESCRIPTION='For a single longitude and latitude point or a region, generate a CSV file from EC surface archive across a span of time -- %s %s' % (AUTHOR, VERSION)

parser = argparse.ArgumentParser(description=PROG_DESCRIPTION)
parser.add_argument('-lon', dest='lon', type=float, help='Longitude of point', required=True)
parser.add_argument('-lat', dest='lat', type=float, help='Latitude of point', required=True)
parser.add_argument('-lon2', dest='lon_e', type=float, help='Longitude of other corner if one wants a region')
parser.add_argument('-lat2', dest='lat_e', type=float, help='Latitude of other corner if one wants a region')
parser.add_argument('-start', dest='start_time', help='RFC3339 time stamp of starting date/time like 2019-10-01T07:00:00Z or 2019-10-01T07:00:00PDT', required=True)
parser.add_argument('-end', dest='end_time', help='RFC3339 time stamp of ending date/time like 2019-10-01T08:00:00Z')
parser.add_argument('-var', dest='var', help='sfc_temp, sfc_pres, or wind')
parser.add_argument('-output', dest='output', help='Output CSV filename')
parser.add_argument('-url', dest='url', help='Default is http://surface.canadarasp.com:8080/data', default='http://surface.canadarasp.com:8080/data')
parser.add_argument('-model', dest='model', help='Default is "hrdps_continental", for GDPS use "glb"', default='hrdps_continental')
parser.add_argument('--localtime', dest='localtime', help='If present', action='store_true')

def send_request(data):
    try:
        r = requests.post(args.url, data=data)
    except requests.exceptions.ConnectionError as e:
        print(f'Error connecting to web server: {e}')
        exit(1)
    try:
        jsondata = json.loads(r.content)
    except Exception as e:
        print(f'Server returned bad JSON {r.content}: {e}')
        quit()
    
    if r.status_code == 200:
        return jsondata
    else:
        print(f'Error returned from web-server: {jsondata["error"]} with reason {jsondata["reason"]}')
        quit()

def get_data_for_region(lona, lata, lonb, latb, start_time, var, model, end_time):
    lon_lat_bbox = '%f, %f, %f, %f' % (lona, lata, lonb, latb)
    query = {'lon-lat-bbox': lon_lat_bbox, 'start-time': start_time, 'end-time': end_time, 'var': var, 'model': model}
    return send_request(query)

def get_data_at_point(lon, lat, start_time, var, model, end_time):
    lon_lat_bbox = '%f, %f' % (lon, lat)
    query = {'lon-lat-bbox': lon_lat_bbox, 'start-time': start_time, 'end-time': end_time, 'var': var, 'model': model}
    return send_request(query)

def write_dicts_to_csv(writeable, data):
    keys = data[0].keys()
    writer = csv.DictWriter(writeable, fieldnames=keys)
    writer.writeheader()
    for datum in data:
        writer.writerow(datum)

args = parser.parse_args()
if args.lon_e and args.lat_e:
    data = get_data_for_region(args.lon, args.lat, args.lon_e, args.lat_e, args.start_time, args.var, args.model,  args.end_time or args.start_time)
else:
    data = get_data_at_point(args.lon, args.lat, args.start_time, args.var, args.model, args.end_time or args.start_time)

if args.localtime: # convert to localtime
    for row in data:
        datetime = iso8601.parse_date(row['time'])
        localdatetime = datetime.astimezone(tzlocal.get_localzone())
        row['time'] = localdatetime.isoformat()

if args.output:
    with open(args.output,'w') as file:
        write_dicts_to_csv(file, data)
else:
    write_dicts_to_csv(sys.stdout, data)
