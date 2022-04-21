import os
import sys
import pycurl
import requests
import json
import stdiomask
import getpass
import pandas as pd
import numpy as np
import datetime
from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

##Dynamic Credentials as input from user ####
#oneview_fqdn = raw_input("Enter FQDN for Oneview:")
#user = raw_input("Enter User Name:")
#passwd = getpass.getpass(prompt="Enter Password:")
#config = {
#    "ip": ('"'+oneview_fqdn+'"'),
#    "credentials": {
#        "userName": ('"'+user+'"'),
#        "password": ('"'+passwd+'"')
#    }
#}
#config = try_load_from_file(config)
#oneview_client = OneViewClient(config)

##Static creds
#config = {
#    "ip": "oneview.fqdn.com"
#    "credentials": {
#        "userName": "hpadmin",
#        "password": "hpinvent"
#    }
#}
#config = try_load_from_file(config)
#oneview_client = OneViewClient(config)

##Suppressing HTTP Request warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


##User Credentials and Oneview FQDN from input Json file config.json#
oneview_client = OneViewClient.from_json_file('config.json')
config = {}
config = try_load_from_file(config)
sgx_date = datetime.datetime.now()
print("Oneview Api Version : {}".format(oneview_client.api_version))
print(config['ip'])
