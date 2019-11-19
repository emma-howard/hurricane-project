#Import All Useful Pakages
import numpy as np 
import pandas as pd
import folium
from folium import IFrame

# Import the raw IBtracs hurricane data stored on GitHub
url = 'https://raw.githubusercontent.com/emma-howard/hurricane-project/master/Dataset/Allstorms.ibtracs_wmo.v03r10.csv'
dataframe = pd.read_csv(url, header = 1)
dataset = dataframe.values
# Coulumns - 
# Who knows | year | num in year | basin | sub_basin | name | yy-mm-dd time | Nature | lat | long | wind (wmo) | pres (wmo) | center
dataset_1980p = dataset[92144:len(dataset)]
# This is an object class to store all the data about storms :) 
class storm(object):

  def __init__(self,name,sid,lat,longi,basin,times,wind,pres): 
    # Note: the lat, long, times, wind, and pres are all arrays across the duration of a storm! 
    self.sid = sid # unique ID number associated with year/number of storm 
    self.name = name # Hurricane Name
    self.lat = lat # Hurricane Latitude, array of all 
    self.longi = longi # Hurricane Longitude, array of all 
    self.basin = basin # Hurricane basin, by 2-lettter code 
    self.times = times #Hurricane times 
    self.wind = wind 
    self.pres = pres 

# This function sorts imported data into storms :) 
def stormify(dataset, storm_list): 
  stormno = -1
  name = 'empty' 
  sid = 1900200
  lat = []
  longi = []
  basin = 'xx'
  times = []
  wind = []
  pres = []
  for item in dataset: 
    # Case 1 - New storm 
    # Create an object for the old storm, re-initialize everything 
    if (item[2] != stormno):
      """    print('Name', name)
      print('SID', sid)
      print('Basin', basin)
      print('Lat', lat)
      print('Long', longi)
      print('Times', times)
      print('Wind', wind)
      print('Pres', pres) """
      # Create an object for the given SID 
      storm_list.append(storm(name, sid, lat, longi, basin, times, wind, pres))
      # Reset Values 
      stormno = item[2]
      name = item[5] 
      sid = str(item[1]*1000 + item[2])
      lat = []
      longi = []
      basin = item[3]
      times = []
      wind = []
      pres = []
    # Case 2 - Same old storm 
    else:
      lat.append(item[8])
      longi.append(item[9])
      times.append(item[6])
      wind.append(item[10])
      pres.append(item[11])

test_set = dataset_1980p
test_list = []
stormify(test_set, test_list)    
