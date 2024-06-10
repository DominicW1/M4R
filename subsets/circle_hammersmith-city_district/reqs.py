import urllib.request
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
import json
import pandas as pd
import datetime
import sys
import base64

env_path = 'key.env'
load_dotenv(dotenv_path=env_path)
key = os.getenv("TFLKEY")
username = os.getenv("RTTUSERNAME")
password = os.getenv("RTTPASSWORD")

def make_request(url):
    try:
        hdr ={
        # Request headers
        'Cache-Control': 'no-cache',
        'app_key': key,
        }

        req = urllib.request.Request(url, headers=hdr)

        req.get_method = lambda: 'GET'
        response = urllib.request.urlopen(req)
        return response
    except Exception as e:
        print(e)
        print(url)
        sys.exit(0)

def make_rtt_request(url):
    try:
        headers = {
            "Cache-Control": "no-cache",
            "Authorization": "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()
        }
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        return response
    except Exception as e:
        print(e)
        print(url)
        sys.exit(0)

# erc = "940GZZLUERC"
# bst = "940GZZLUBST"

# # get the timetable for the circle line
# url = f"https://api.tfl.gov.uk/Line/circle/Timetable/940GZZLUERC/to/940GZZLUPAH"
# response = make_request(url)
# data = json.loads(response.read())
# # dump the data to a json file
# with open('data3.json', 'w') as f:
#     json.dump(data, f, indent=4)


# response = make_rtt_request("https://api.rtt.io/api/v1/json/search/AMR/2024/05/29")
# data = json.loads(response.read())
# # dump the data to a json file
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4)

# euston_services = []
# watford_services = []
# east_croydon_services = []
# clapham_junction_services = []

# for service in data["services"]:
#     service_loc = service["locationDetail"]
#     checks = [service["isPassenger"], service_loc["isPublicCall"], service["serviceType"] == "train", (service["atocCode"] == "LO" or service["atocCode"] == "SN")]
#     if all(checks):
#         hhmm_time = service_loc["gbttBookedDeparture"]
#         # convert to datetime time object
#         time = datetime.datetime.strptime(hhmm_time, "%H%M").time()
#         # if time before 0400
#         if time < datetime.time(4, 0):
#             continue
#         destination = service_loc["destination"][0]["description"]
#         if destination == "Watford Junction":
#             watford_services.append(time)
#         elif destination == "London Euston":
#             euston_services.append(time)
#         elif destination == "East Croydon":
#             east_croydon_services.append(time)
#         else:
#             clapham_junction_services.append(time)

# print("Euston Services")
# print(euston_services)
# print("Watford Services")
# print(watford_services)
# print("East Croydon Services")
# print(east_croydon_services)
# print("Clapham Junction Services")
# print(clapham_junction_services)

# wimbledon = "940GZZCRWMB"
# morden_road = "940GZZCRMDN"
# line = "tram"

# import time

# url = f"https://api.tfl.gov.uk/Line/{line}/Timetable/{morden_road}/to/{wimbledon}"
# for i in range(100):
#     try:
#         response = make_request(url)
#         print("success")
#     except Exception as e:
#         print(e)
#         print("failed")
#         continue

#     time.sleep(1)
# data = json.loads(response.read())
# # dump the data to a json file
# with open('data2.json', 'w') as f:
#     json.dump(data, f, indent=4)
