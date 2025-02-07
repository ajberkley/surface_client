# surface_client
A Python client to interface with surface.canadarasp.com which serves archived HRDPS surface data.  This modified client provides grabbing data by the initialization time of the model and works against a temporary endpoint.

# Downloading from git:
```
git clone https://github.com/ajberkley/surface_client.git; cd surface_client; git checkout full-history
```
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

Getting one variable at a single point over a time sequence and emitting to a CSV file

```python surface_client.py -lon -122.0 -lat 48.0 -initstart 2024-06-23T00:00:00Z -initend 2024-06-23T12:00:00Z -var wind -output blarg.csv```

If the download is interrupted, repeat the call above and it will scan the output file for the missing data and continue.  initstart and initend must have an hour indicator of 00, 06, 12, or 18, the initialization hours of the HRDPS model.
