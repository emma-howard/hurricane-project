import tensorflow as tf
import numpy as np
import pandas as pd
import folium
import datetime as dt
import dateutil.parser
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

  def Get_Maxs(this):
    maxLat = max(this.lat)
    maxLong = max(this.longi)
    maxWind = max(this.wind)
    maxPres = max(this.pres)
    return maxLat, maxLong, maxWind, maxPres

  def Get_Mins(this):
    minLat = min(this.lat)
    minLong = min(this.longi)
    minWind = min(this.wind)
    minPres = min(this.pres)
    return minLat, minLong, minWind, minPres


  def CleanStorm(this,interval):
    toRemove = []
    i = 1
    lastCleanTime = this.times[0]
    while(i < len(this.times)):
      nextTime = this.times[i]
      tDelta = nextTime - lastCleanTime
      if tDelta == interval:
        lastCleanTime = nextTime
      else:
        toRemove.append(i)
      i += 1

    toRemove.sort(reverse=True)
    for r in toRemove:
      this.times.pop(r)
      this.longi.pop(r)
      this.lat.pop(r)
      this.wind.pop(r)
      this.pres.pop(r)      

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
      times = [dateutil.parser.parse(item[6])]
      wind = [item[10]]
      pres = [item[11]]
    # Case 2 - Same old storm 
    else:
      lat.append(item[8])
      longi.append(item[9])
      times.append(dateutil.parser.parse(item[6]))
      wind.append(item[10])
      pres.append(item[11])

  return storm_list

def normalize(x, mx, mn):
  return (x-mn)/(mx-mn)

def normalize_col(col,maxV,minV):
  for i in range(len(col)):
    col[i] = normalize(col[i],maxV,minV)
  return col

def normalize_storms(storms):
  maxLats = []
  maxLongs = []
  maxWinds = []
  maxPress = []

  minLats = []
  minLongs = []
  minWinds = []
  minPress = []

  for s in storms:
    maLa , maLo , maWi, maPr = s.Get_Maxs()
    maxLats.append(maLa)
    maxLongs.append(maLo)
    maxWinds.append(maWi)
    maxPress.append(maPr)

    miLa, miLo, miWi, miPr = s.Get_Mins()
    minLats.append(miLa)
    minLongs.append(miLo)
    minWinds.append(miWi)
    minPress.append(miPr)

  maxs = [max(maxLats),max(maxLongs),max(maxWinds),max(maxPress)]
  mins = [min(minLats),min(minLongs),min(minWinds),min(minPress)]

  for s in storms:
    s.lat = normalize_col(s.lat,maxs[0],mins[0])
    s.longi = normalize_col(s.longi,maxs[1],mins[1])
    s.wind = normalize_col(s.wind,maxs[2],mins[2])
    s.pres = normalize_col(s.pres,maxs[3],mins[3])

  return storms, maxs, mins

def remove_small_storms(storm_list,cutoff):
  refined_storms = []
  for storm in storm_list:
    if len(storm.longi) >= cutoff:
      refined_storms.append(storm)
  return refined_storms 

def get_orgnaised_storm(storm,size):
  #basin_codes = ["","SE","SI","SP","EP","WP","NA","NI","SA"]
  #sub_basin_codes = ["","MM","WA","EA","CP","NA","GM","CS","BB","AS"]
  datas = []
  labels = []

  #basin = basin_codes.index(storm.basin)
  #sub_basin = sub_basin_codes.index(storm.sub_basin)

  lats = storm.lat
  longs = storm.longi

  winds = storm.wind
  press = storm.pres
  
  length = len(winds)
  for i in range((length+1)-size):
    new_data = []
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

class model():
  def __init__(self, maxs, mins):
    self.maxs = maxs
    self.mins = mins 

  def unNormalize(self,data):
    orig = []
    for d, maxV, minV in zip(data,self.maxs,self.mins):
      o = d * (maxV - minV) + minV
      orig.append(o)
    return orig
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                            Data Visualization                                #

#------------------------------------------------------------------------------#

def main():
  # Import the raw IBtracs hurricane data stored on GitHub
  url = 'https://raw.githubusercontent.com/emma-howard/hurricane-project/master/Dataset/Allstorms.ibtracs_wmo.v03r10.csv'
  cols = ['sid','year','num','basin','sub_basin','name','time','Nature','lat','long','wind','pres', "center","wind %", "pres %","Center"]
  df = pd.read_csv(url, skiprows= 1, header=1)
  # Coulumns - 
  # Who knows | year | num in year | basin | sub_basin | name | yy-mm-dd time | Nature | lat | long | wind (wmo) | pres (wmo) | center

  basin = "NA"
  df["BB"] = df["BB"].apply(str.strip)
  df = df.loc[df["BB"] == basin] # get only NA basin
  df = df.loc[df["kt"] > 0] # Remove remove invalid data
  df = df.loc[df["mb"] > 0] # Remove remove invalid data

  min_year = 1980
  dataset_1980p = df.loc[df["Year"] >= min_year]

  raw_data = dataset_1980p.values

  sorted_storms = stormify(raw_data)

  interval = dt.timedelta(hours=6)
  for s in sorted_storms:
    s.CleanStorm(interval)
  
  storm_size = 5 # 4 previous time intervals, 1 for next iterval 
  sorted_storms = remove_small_storms(sorted_storms,storm_size)

  sorted_storms, maxs, mins = normalize_storms(sorted_storms)
  
  data_x, data_y = create_organised_data(sorted_storms,storm_size)
  
  print(data_x[-1])
  print(data_y[-1])
  print("---")
  print(sorted_storms[-1].lat)
  print(sorted_storms[-1].longi)
  
main()
