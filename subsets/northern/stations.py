import numpy as np
import reqs as reqs
import json
import pickle
import sys
import os
from icecream import ic

lines = ["northern"]

def get_dict(lines):
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

    # station_dict["Morden_tram"] = "940GZZCRMDN"
    # station_dict["Wimbledon_tram"] = "940GZZCRWMB"

    return station_dict, all_stations

def get_nr_dict():
    nr_station_dict = {}

    nr_station_dict["Amersham"] = "AMR"
    nr_station_dict["Chalfont & Latimer"] = "CFO"
    nr_station_dict["Chorleywood"] = "CLW"
    nr_station_dict["Rickmansworth"] = "RIC"
    nr_station_dict["Harrow & Wealdstone"] = "HRW"
    nr_station_dict["Kenton"] = "KNT"
    nr_station_dict["South Kenton"] = "SOK"
    nr_station_dict["North Wembley"] = "NWB"
    nr_station_dict["Wembley Central"] = "WMB"
    nr_station_dict["Stonebridge Park"] = "SBP"
    nr_station_dict["Harlesden"] = "HDN"
    nr_station_dict["Willesden Junction"] = "WIJ"
    nr_station_dict["Kensal Green"] = "KNL"
    nr_station_dict["Queen's Park"] = "QPW"
    nr_station_dict["West Ham"] = "WEH"
    nr_station_dict["Barking"] = "BKG"
    nr_station_dict["Upminster"] = "UPM"
    nr_station_dict["Old Street"] = "OLD"
    nr_station_dict["Highbury & Islington"] = "HHY"
    nr_station_dict["Walthamstow Queens Road"] = "WMW"
    nr_station_dict["Leytonstone High Road"] = "LER"
    nr_station_dict["Shepherd's Bush (Central)"] = "SPB"
    nr_station_dict["Kensington (Olympia)"] = "KPA"
    nr_station_dict["West Brompton"] = "WBP"
    nr_station_dict["Richmond"] = "RMD"
    nr_station_dict["Kew Gardens"] = "KWG"
    nr_station_dict["Gunnersbury"] = "GUN"
    # add lizzy line stations

    # sort the dictionary by station name
    nr_station_dict = dict(sorted(nr_station_dict.items()))
    return nr_station_dict


save = 0
load = 1

local_dir = os.path.dirname(__file__)

if save and load:
    print("no")
    sys.exit(0)
elif save:
    station_dict, all_stations = get_dict(lines)
    path = os.path.join(local_dir, "pickles/station_dict.pkl")
    with open(path, "wb") as f:
        pickle.dump(station_dict, f)
    path = os.path.join(local_dir, "pickles/all_stations.pkl")
    with open(path, "wb") as f:
        pickle.dump(all_stations, f)
    path = os.path.join(local_dir, "pickles/nr_station_dict.pkl")
    with open(path, "wb") as f:
        nr_station_dict = get_nr_dict()
        pickle.dump(nr_station_dict, f)
elif load:
    path = os.path.join(local_dir, "pickles/station_dict.pkl")
    with open(path, "rb") as f:
        station_dict = pickle.load(f)
    path = os.path.join(local_dir, "pickles/all_stations.pkl")
    with open(path, "rb") as f:
        all_stations = pickle.load(f)
    path = os.path.join(local_dir, "pickles/nr_station_dict.pkl")
    with open(path, "rb") as f:
        nr_station_dict = pickle.load(f)
else:
    station_dict, all_stations = get_dict(lines)
    nr_station_dict = get_nr_dict()
