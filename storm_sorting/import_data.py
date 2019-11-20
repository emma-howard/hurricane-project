import tensorflow as tf
import numpy as np
import pandas as pd
import folium 
tf.__version__

#------------------------------------------------------------------------------#
#                               Data Processing                                #



# This is an object class to store all the data about storms :) 
class storm(object):

  def __init__(self,name,sid,lat,longi,basin,sub_basin,times,wind,pres): 
    # Note: the lat, long, times, wind, and pres are all arrays across the duration of a storm! 
    self.sid = sid # unique ID number associated with year/number of storm 
    self.name = name # Hurricane Name
    self.lat = lat # Hurricane Latitude, array of all 
    self.longi = longi # Hurricane Longitude, array of all 
    self.basin = basin # Hurricane basin, by 2-lettter code 
    self.sub_basin = sub_basin
    self.times = times #Hurricane times 
    self.wind = wind 
    self.pres = pres 

# This function sorts imported data into storms :) 
def stormify(dataset):
  storm_list = []
  item = dataset[0] 

  stormno = item[2]
  name = item[5] 
  sid = str(item[1]*1000 + item[2])
  lat = []
  longi = []
  basin = str.strip(item[3])
  sub_basin = str.strip(item[4])
  print(sub_basin)
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
      storm_list.append(storm(name, sid, lat, longi, basin,sub_basin, times, wind, pres))
      # Reset Values with new data
      stormno = item[2]
      name = item[5] 
      sid = str(item[1]*1000 + item[2])
      lat = [item[8]]
      longi = [item[9]]
      basin = str.strip(item[3])
      sub_basin = str.strip(item[4])
      times = [item[6]]
      wind = [item[10]]
      pres = [item[11]]
    # Case 2 - Same old storm 
    else:
      lat.append(item[8])
      longi.append(item[9])
      times.append(item[6])
      wind.append(item[10])
      pres.append(item[11])

  return storm_list

def remove_small_storms(storm_list,cutoff):
  refined_storms = []
  for storm in storm_list:
    if len(storm.longi) >= cutoff:
      refined_storms.append(storm)
  return refined_storms 

def get_orgnaised_storm(storm,size):
  basin_codes = ["","SE","SI","SP","EP","WP","NA","NI","SA"]
  sub_basin_codes = ["","MM","WA","EA","CP","NA","GM","CS","BB","AS"]
  datas = []
  labels = []

  basin = basin_codes.index(storm.basin)
  sub_basin = sub_basin_codes.index(storm.sub_basin)

  lats = storm.lat
  longs = storm.longi

  winds = storm.wind
  press = storm.pres
  
  length = len(winds)
  for i in range((length+1)-size):
    new_data = [basin,sub_basin]
    for j in range(size-1):
      index = j + i

      new_data.append(lats[index])
      new_data.append(longs[index])

      new_data.append(winds[index])
      new_data.append(press[index])

    label_index = i + size - 1 
    label = [lats[label_index],longs[label_index]]

    datas.append(new_data)
    labels.append(label)

  return datas, labels

def create_organised_data(storm_list, stormSize):
  data_x = [] # basin_code|sub_basin_code|lat_t0|long_t0|wnd_t0|pres_t0|lat_t1|long_t1|wnd_t1|pres_t1|...
  data_y = [] # lat at next interval | long at next interval

  for storm in storm_list:
    x, y = get_orgnaised_storm(storm,stormSize)
    data_x = data_x + x
    data_y = data_y + y

  return data_x, data_y


#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                                   Model                                      #

#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                            Data Visualization                                #

#------------------------------------------------------------------------------#

def main():
  # Import the raw IBtracs hurricane data stored on GitHub
  url = 'https://raw.githubusercontent.com/emma-howard/hurricane-project/master/Dataset/Allstorms.ibtracs_wmo.v03r10.csv'
  cols = ['sid','year','num','basin','sub_basin','name','time','Nature','lat','long','wind','pres', "center"]
  df = pd.read_csv(url, skiprows= 2)
  print(df.head())
  # Coulumns - 
  # Who knows | year | num in year | basin | sub_basin | name | yy-mm-dd time | Nature | lat | long | wind (wmo) | pres (wmo) | center
  min_year = 1980
  dataset_1980p = df.loc[df["Year"] >= min_year]
  raw_data = dataset_1980p.values
  sorted_storms = stormify(raw_data)

  storm_size = 5 # 4 previous time intervals, 1 for next iterval 
  sorted_storms = remove_small_storms(sorted_storms,storm_size)
  B = []
  SB = []
  for s in sorted_storms:
    b = s.basin
    sb = s.sub_basin

    if b not in B:
      B.append(b)
    if sb not in SB: 
      SB.append(sb)
    
  print(B)
  print(SB)

  data_x, data_y = create_organised_data(sorted_storms,storm_size)
  print(data_x[-1])
  print(data_y[-1])
  print("---")
  print(sorted_storms[-1].lat)
  print(sorted_storms[-1].longi)
  
main()
