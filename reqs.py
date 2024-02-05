import urllib.request
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
import json
import pandas as pd
import datetime

env_path = 'key.env'
load_dotenv(dotenv_path=env_path)
key = os.getenv("TFLKEY")

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
        return None
