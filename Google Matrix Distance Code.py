#import all the things
import pandas as pd
import json
import urlopen from urllib2 as req
import os
import datetime from datetime as dt
import strftime from datetime as sft

#put the api key here
key = 'APIKEYGOESHERE'

#origin is set here
origins = 'Canberra+ACT'

#read list of destinations to a dataframe with 3 columns
names = ['Destination', 'Duration', "Distance"]
df = pd.read('destinations.xlsx', skiprows = 1, names = names)
 
#iterate through the locations, sending the request and capturing the response
#note it may be more inefficient doing it this way - but this gets around the maximum combinations per request
#and requests are billed per combination, not per request i.e. it costs the same
for index, row in df.iterrows():
    destinations = row["Destination"].str.replace(' ', '+')
    matrix = "origins=" + origins + "&destinations=" + destinations
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?" + matrix + "&units=metric&key=" + key
    
    #make the request and parse the result to python datastructure (lists and dictionaries)
    response = req(url)
    parsed = json.loads(response)
    
    #extract the duration and distance data and add to the destination record
    df.loc[row, 'Duration'] = parsed["rows"]["elements"]["duration"]["text"]
    df.loc[row, 'Distance'] = parsed["rows"]["elements"]["distance"]["value"]/1000

#export the data to a csv file  
fileName = 'Distance-Matrix-Output_' + dt.now().sft("%Y-%m%d_%H-%M") 
df.to_csv(os.path.join(sys.path[0],fileName), header=names, index=False)