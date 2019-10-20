# surface_client
A Python client to interface with surface.canadarasp.com which serves archived HRDPS surface data.

To install on a unix machine:
# Make sure you have python 3.7 installed
sudo apt-get install python3.7  # Ubuntu
sudo dnf install python37 # Fedora 

For windows (untested):
Install python 3.7.  Start a command shell

git clone https://github.com/ajberkley/surface_client.git
cd surface_client
virtualenv -p `which python3.7` env # or python3.7 -m venv env
source env/bin/activate
pip install -r requirements.txt
python surface_client.py -h
python surface_client.py -lon -122.0 -lat 48.0 -start 2019-10-03T00:00:00Z -end 2019-10-03T01:00:00Z -var sfc_temp
python surface_client.py -lon -122.0 -lat 48.0 -lon2 -122.01 -lat2 48.1 -start 2019-10-03T00:00:00Z -end 2019-10-03T01:00:00Z -var wind

