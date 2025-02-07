# PYTHON 3.7
import iso8601
import requests
import csv
import json
import argparse
import sys
import tzlocal
import datetime
VERSION="v0.9a Feb 2025"
AUTHOR="Andrew Berkley (ajberkley@gmail.com)"

PROG_DESCRIPTION='For a single longitude and latitude point or a region, generate a CSV file from a single variable from the EC surface archive across a span of time -- %s %s' % (AUTHOR, VERSION)

parser = argparse.ArgumentParser(description=PROG_DESCRIPTION)
parser.add_argument('-lon', dest='lon', type=float, help='Longitude of point')
parser.add_argument('-lat', dest='lat', type=float, help='Latitude of point')
parser.add_argument('-lon2', dest='lon_e', type=float, help='Longitude of other corner if one wants a region')
parser.add_argument('-lat2', dest='lat_e', type=float, help='Latitude of other corner if one wants a region')
parser.add_argument('-initstart', dest='init_time_start', help='RFC3339 time stamp of HRDPS run like 2019-10-01T06:00:00Z.  Possible init hours are 0, 6, 12, 18.')
parser.add_argument('-initend', dest='init_time_end', help='RFC3339 time stamp of HRDPS run like 2019-10-01T06:00:00Z.  Possible final hours are 0, 6, 12, 18.')
parser.add_argument('-var', dest='var', help='sfc_temp, sfc_pres, wind, max_gust, or sfc_prate.  call this with --variables to get up to date list.')
parser.add_argument('-output', dest='output', help='Output CSV filename.  If the file exists, it will be appended to after adjusting initstart to be past the last date of any initialization date in the file.')
parser.add_argument('-url', dest='url', help='Default is http://surface.canadarasp.com:8090/', default='http://surface.canadarasp.com:8090/')
parser.add_argument('-model', dest='model', help='Default is "hrdps_continental", for GDPS use "glb"', default='hrdps_continental')
parser.add_argument('--localtime', dest='localtime', help='Convert data timestamps to local timezone', action='store_true')
parser.add_argument('--variables', dest='variables', help='List all available variables', action='store_true')

def send_request(data, output_func, endpoint="data"):
    try:
        url = args.url.strip('/') + '/' + endpoint
        r = requests.post(url, data=data, stream=True)
    except requests.exceptions.ConnectionError as e:
        print(f'Error connecting to web server: {e}')
        exit(1)
    try:
        if r.status_code == 200:
            for chunk in r.iter_content(chunk_size=None):
                jsondata = json.loads(chunk)
                if("error" in jsondata):
                    print(f'Error returned from web-server: {jsondata["error"]} with reason {jsondata["reason"]}')
                    quit()
                output_func(jsondata)
        else:
            print(f'Server returned error code {r.status_code}')
            quit()
    except Exception as e:
        print(f'Server returned bad JSON: {chunk}')
        quit()

def get_data_for_region(lona, lata, lonb, latb, init_time_start, init_time_end, var, model, output):
    lon_lat_bbox = '%f, %f, %f, %f' % (lona, lata, lonb, latb)
    query = {'lon-lat-bbox': lon_lat_bbox, 'init-time-start': init_time_start, 'init-time-end': init_time_end, 'var': var, 'model': model}
    return send_request(query, output)

def get_data_at_point(lon, lat, init_time_start, init_time_end, var, model, output):
    lon_lat_bbox = '%f, %f' % (lon, lat)
    query = {'lon-lat-bbox': lon_lat_bbox, 'init-time-start': init_time_start, 'init-time-end': init_time_end, 'var': var, 'model': model}
    return send_request(query, output)

def get_variables(output_func):
    send_request(None, output_func, endpoint="variables")

wrote_header = False
    
def write_dicts_to_csv(writeable, data):
    global wrote_header
    keys = data[0].keys()
    writer = csv.DictWriter(writeable, fieldnames=keys)
    if not wrote_header:
        writer.writeheader()
        wrote_header = True
    for datum in data:
        writer.writerow(datum)

def convert_to_localtime(data):
    if args.localtime: # convert to localtime
        for row in data:
            datetime = iso8601.parse_date(row['time'])
            localdatetime = datetime.astimezone(tzlocal.get_localzone())
            row['time'] = localdatetime.isoformat()
    return data

def write_to_csv(data):
    if args.output:
        with open(args.output,'a+') as file:
            write_dicts_to_csv(file, data)
    else:
        write_dicts_to_csv(sys.stdout, data)
    return data

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

def output_variables(data):
    for var, desc in data.items():
        print('%-10s %-10s' % (var, desc))

if args.variables:
    print('Available variables are:')
    get_variables(output_variables)
    exit(0)

if not (args.lon and args.lat and args.init_time_start):
    print('Need -lon -lat and -initstart')
    
if args.output: # Does the file have any data already?
    try:
        with open(args.output,'r') as file:
            reader = csv.DictReader(file)
            original_start_time = args.init_time_start
            notified = False
            for row in reader:
                wrote_header = True
                start_time = iso8601.parse_date(args.init_time_start)
                if row['inittime'] != "unavailable":
                    data_time = iso8601.parse_date(row['inittime'])
                    if data_time >= start_time:
                        data_time = data_time + datetime.timedelta(hours=6)
                        if not notified:
                            notified = True
                            print('There is existing data in output file, updating initstart')
                        args.init_time_start = data_time.isoformat()
            if notified:
                print(f'Updated initstart from {original_start_time} to {args.init_time_start}')
                
    except FileNotFoundError:
        pass
    except NameError:
        print('Output file has wrong format, we are appending data to it anyway')
        pass

def writer(data):
    write_to_csv(convert_to_localtime(data))

if args.lon_e and args.lat_e:
    get_data_for_region(args.lon, args.lat, args.lon_e, args.lat_e, args.init_time_start, args.init_time_end or args.init_time_start, args.var, args.model, writer)
else:
    get_data_at_point(args.lon, args.lat, args.init_time_start, args.init_time_end or args.init_time_start, args.var, args.model, writer)

