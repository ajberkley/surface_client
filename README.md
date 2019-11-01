# surface_client
A Python client to interface with surface.canadarasp.com which serves archived HRDPS surface data.

# Downloading from git:

git clone https://github.com/ajberkley/surface_client.git

# Installation on UNIX
To install on a unix machine:
```
# Make sure you have python 3.7 installed
sudo apt-get install python3.7  # Ubuntu
sudo dnf install python37 # Fedora 
```
Then
```
cd surface_client
virtualenv -p `which python3.7` env # or python3.7 -m venv env
source env/bin/activate

# Installation on Windows
For windows: Install python 3.7.  Start a command shell and navigate to where you have
downloaded or installed the surface_client code, then type the following:
```
pip install virtualenv
virtualenv env
env\Scripts\activate
python surface_client.py
```

# Running on both types
```
pip install -r requirements.txt
python surface_client.py -h
python surface_client.py -lon -122.0 -lat 48.0 -start 2019-10-03T00:00:00Z -end 2019-10-03T01:00:00Z -var sfc_temp
python surface_client.py -lon -122.0 -lat 48.0 -lon2 -122.01 -lat2 48.1 -start 2019-10-03T00:00:00Z -end 2019-10-03T01:00:00Z -var wind
```

To obtain timestamps in local time:
python surface_client.py --localtime -lon -122.0 -lat 48.0 -lon2 -122.01 -lat2 48.1 -start 2019-10-03T00:00:00Z -end 2019-10-03T01:00:00Z -var wind

To output to a file:
python surface_client.py --localtime -lon -122.0 -lat 48.0 -lon2 -122.01 -lat2 48.1 -start 2019-10-03T00:00:00Z -end 2019-10-03T01:00:00Z -var wind -output output.csv
