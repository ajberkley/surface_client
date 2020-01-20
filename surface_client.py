# PYTHON 3.7
import iso8601
import requests
import csv
import json
import argparse
import sys
import tzlocal
import datetime
VERSION="v0.9 January 2020"
AUTHOR="Andrew Berkley (ajberkley@gmail.com)"

PROG_DESCRIPTION='For a single longitude and latitude point or a region, generate a CSV file from a single variable from the EC surface archive across a span of time -- %s %s' % (AUTHOR, VERSION)

parser = argparse.ArgumentParser(description=PROG_DESCRIPTION)
parser.add_argument('-lon', dest='lon', type=float, help='Longitude of point')
parser.add_argument('-lat', dest='lat', type=float, help='Latitude of point')
parser.add_argument('-lon2', dest='lon_e', type=float, help='Longitude of other corner if one wants a region')
parser.add_argument('-lat2', dest='lat_e', type=float, help='Latitude of other corner if one wants a region')
parser.add_argument('-start', dest='start_time', help='RFC3339 time stamp of starting date/time like 2019-10-01T07:00:00Z or 2019-10-01T07:00:00-07:00')
parser.add_argument('-end', dest='end_time', help='RFC3339 time stamp of ending date/time like 2019-10-01T08:00:00Z')
parser.add_argument('-var', dest='var', help='sfc_temp, sfc_pres, wind, max_gust, or sfc_prate.  call this with --variables to get up to date list.')
parser.add_argument('-output', dest='output', help='Output CSV filename.  If the file exists, it will be appended to after adjusting start_time to be past the last date of any data in the file.')
parser.add_argument('-url', dest='url', help='Default is http://surface.canadarasp.com:8080/', default='http://surface.canadarasp.com:8080/')
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

def get_data_for_region(lona, lata, lonb, latb, start_time, var, model, end_time, output):
    lon_lat_bbox = '%f, %f, %f, %f' % (lona, lata, lonb, latb)
    query = {'lon-lat-bbox': lon_lat_bbox, 'start-time': start_time, 'end-time': end_time, 'var': var, 'model': model}
    return send_request(query, output)

def get_data_at_point(lon, lat, start_time, var, model, end_time, output):
    lon_lat_bbox = '%f, %f' % (lon, lat)
    query = {'lon-lat-bbox': lon_lat_bbox, 'start-time': start_time, 'end-time': end_time, 'var': var, 'model': model}
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

if not (args.lon and args.lat and args.start_time):
    print('Need -lon -lat and -start_time')
    
if args.output: # Does the file have any data already?
    try:
        with open(args.output,'r') as file:
            reader = csv.DictReader(file)
            original_start_time = args.start_time
            notified = False
            for row in reader:
                wrote_header = True
                start_time = iso8601.parse_date(args.start_time)
                data_time = iso8601.parse_date(row['time'])
                if data_time >= start_time:
                    data_time = data_time + datetime.timedelta(hours=1)
                    if not notified:
                        notified = True
                        print('There is existing data in output file, updating start_time')
                    args.start_time = data_time.isoformat()
            if notified:
                print(f'Updated start_time from {original_start_time} to {args.start_time}')
                
    except FileNotFoundError:
        pass
    except NameError:
        print('Output file has wrong format, we are appending data to it anyway')
        pass

def writer(data):
    write_to_csv(convert_to_localtime(data))

if args.lon_e and args.lat_e:
    get_data_for_region(args.lon, args.lat, args.lon_e, args.lat_e, args.start_time, args.var, args.model,  args.end_time or args.start_time, writer)
else:
    get_data_at_point(args.lon, args.lat, args.start_time, args.var, args.model, args.end_time or args.start_time, writer)

