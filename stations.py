import numpy as np
import reqs
import json

lines = ["bakerloo", "central", "circle", "district", "hammersmith-city", "jubilee", "metropolitan", "northern", "piccadilly", "victoria", "waterloo-city"]

all_stations = []

for line in lines:
    url = f"https://api.tfl.gov.uk/Line/{line}/StopPoints?tflOperatedNationalRailStationsOnly=false"
    response = reqs.make_request(url)
    json_data = json.loads(response.read())
    # list of station name, id pairs
    stat_id = [(dic["commonName"], dic["id"]) for dic in json_data]
    # concatenate to all_stations
    all_stations += stat_id

# remove duplicates from all_stations
all_stations = np.array(list(set(all_stations)))

# replace 'Paddington (H&C Line)-Underground' with 'Paddington (H&C Line) Underground Station'
all_stations[:,0] = [name.replace("Paddington (H&C Line)-Underground", "Paddington (H&C Line) Underground Station") for name in all_stations[:,0]]

# remove " Underground Station" from station names
all_stations[:,0] = [name[:-20] for name in all_stations[:,0]]

# create a dictionary of stations, id pairs
station_dict = {name: id for name, id in all_stations}