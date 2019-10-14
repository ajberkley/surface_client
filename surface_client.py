# PYTHON 3.7
import requests
import csv
import json
URL='http://surface.canadarasp.com:8080/data'

def get_data_at_point(lon, lat, start_time, end_time=None):
    lon_lat_bbox = '%f, %f' % (lon, lat)
    query = {'lon-lat-bbox': lon_lat_bbox, 'start-time': start_time, 'end-time': end_time or start_time}
    r = requests.post(URL, data=query)
    return json.loads(r.content)

def write_dicts_to_csv(file, data):
    keys = data[0].keys()
    with open(file,'w') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for datum in data:
            writer.writerow(datum)

write_dicts_to_csv('blarg.csv',get_data_at_point(-122.43, 48.0, '2019-10-01T07:00:00Z', '2019-10-01T08:00:00Z'))
