# surface_client
A Python client to interface with surface.canadarasp.com which serves archived HRDPS surface data.  This modified client provides grabbing data by the initialization time of the model and works against a temporary endpoint.

# Downloading from git:

git clone https://github.com/ajberkley/surface_client.git; git checkout full-history

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
pip install -r requirements.txt
```

# Installation on Windows
For windows: Install python 3.7.  Start a command shell and navigate to where you have
downloaded or installed the surface_client code, then type the following:
```
pip install virtualenv
virtualenv env
env\Scripts\activate
pip install -r requirements.txt
python surface_client.py
```

# Usage
To get a list of options:

```python surface_client.py -h```

Getting one variable at a single point over a time sequence

```python surface_client.py -lon -122.0 -lat 48.0 -start 2019-12-23T00:00:00Z -end 2019-12-23T01:00:00Z -var sfc_temp```

Getting one variable at a single point over a time sequence, specifying time in PST:

```python surface_client.py -lon -122.0 -lat 48.0 -start 2019-12-23T07:00:00-07:00 -end 2019-12-23T08:00:00-07:00 -var sfc_temp```

Getting a variable across a rectangular region over a time sequence:

```python surface_client.py -lon -122.0 -lat 48.0 -lon2 -122.01 -lat2 48.1 -start 2019-12-23T00:00:00Z -end 2019-12-23T01:00:00Z -var wind```

To have the output timestamps converted from UTC time to local time:

```python surface_client.py --localtime -lon -122.0 -lat 48.0 -lon2 -122.01 -lat2 48.1 -start 2019-12-23T00:00:00Z -end 2019-12-23T01:00:00Z -var wind```

To output to a file:

```python surface_client.py --localtime -lon -122.0 -lat 48.0 -lon2 -122.01 -lat2 48.1 -start 2019-12-23T00:00:00Z -end 2019-12-23T01:00:00Z -var wind -output output.csv```
