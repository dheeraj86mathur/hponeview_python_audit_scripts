# -*- coding: utf-8 -*-
###
###
import os
import pycurl
import requests
from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file
config = {
    "ip": "oneview.fqdn.com",
    "credentials": {
        "userName": "hpadmin",
        "password": "hpinvent"
    }
}

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Try load config from a file (if there is a config file)
config = try_load_from_file(config)

#options = {
#    "hostname": config['server_hostname'],
#    "username": config['server_username'],
#    "password": config['server_password'],
#    "licensingIntent": "OneView",
#    "configurationState": "Managed"
#}

# Set the server_hardware_id to run this example.
# server_hardware_id example: 37333036-3831-4753-4831-30315838524E
#server_hardware_id = "30373237-3132-4753-4835-333457564A44"
#uri = '/rest/server-hardware/30373237-3132-4753-4835-333457564A44'
#server_hardware_id = "37383638-3330-4753-4838-31345637444B"
oneview_client = OneViewClient(config)
server_hardwares = oneview_client.server_hardware

# Get list of all server hardware resources
#print("Get list of all server hardware resources")
#server_hardware_all = oneview_client.server_hardware.get_all()
#print( server_hardware_all )
#for serv in server_hardware_all:
#    print('%s' % (serv['name'], serv['uri']))
#     print(" '%s'.\t  uri = '%s'.\t '%s'" % (serv['name'], serv['uri'], serv['serverName']))
#server_name = "C3G19ENC2, bay 1"
server_name = "ILOSGH815X7F5.sgp.hp.mfg"
server = server_hardwares.get_by_name(server_name)
#print("This script will get the sso token for ilO remote console for server hardware : '%s'" % (server_name))
# Get URL to launch SSO session for iLO web interface

#if server:
#    ilo_sso_url = server.get_ilo_sso_url()
#    print("URL to launch a Single Sign-On (SSO) session for the iLO web interface for server at uri:\n","{}\n   '{}'".format(server.data['uri'], ilo_sso_url))

#curl --location -g --request GET '{{ilo_sso_url}}/redfish/v1/AccountService/Accounts/ ' \
#--header 'OData-Version: 4.0' \
#--header 'Content-Type: application/json' \
#--header '-X-Auth-Token: {{Token}}' 
# Get URL to launch SSO session for iLO Integrated Remote Console
# Application (IRC)
# You can also specify ip or consoleType if you need, inside function get_remote_console_url()
if server:
    remote_console_url = server.get_remote_console_url()
#    print("URL to launch a Single Sign-On (SSO) session for iLO Integrated Remote Console Application",
#          "for server with name :\n   {}   '{}'".format(server.data['serverName'], remote_console_url))
ilo = remote_console_url['remoteConsoleUrl'].split("=")
ilo_ip = ('https://'+ilo[1].split("&")[0])
ilo_all_accounts_url = (ilo_ip+'/redfish/v1/AccountService/Accounts/')
#ilo_sessionurl = (ilo_ip+'/redfish/v1/AccountService/Accounts/1')
#print(ilo_all_accounts_url)
auth_token = ilo[2]
my_headers = {'X-Auth-Token': auth_token, 'OData-Version': '4.0', 'Content-Type': 'application/json'}
#response = requests.get(ilo_ip, headers=my_headers)
#response = requests.get(ilo_sessionurl, headers=my_headers, verify = False)
response = requests.get(ilo_all_accounts_url, headers=my_headers, verify = False)
#session = requests.Session()
#session.headers.update({'Authorization': 'Bearer {auth_token}'})
#response = session.get(ilo_ip)
#print("JSON response for server Accounts is: \n '%s'" % (response.json()))
json_data = response.json()
print("Count of local Users on the ILO for server name:  {} :  {}".format(server.data['serverName'], json_data['Members@odata.count']))
#print("List of Members: \n  {}".format(json_data['Members']))
#response = requests.get("http://api.open-notify.org/astros.json")
#print(response)
for members in json_data['Members']:
#    print('%s' % (members['@odata.id']))
    ilo_sessionurl = (ilo_ip+members['@odata.id'])
#    print(ilo_sessionurl)
    res_local_users = requests.get(ilo_sessionurl, headers=my_headers, verify = False)
    json_local_users = res_local_users.json()
#    print("User : {} :: Privileges : {}".format(json_local_users["UserName"], json_local_users["Oem"]["Hp"]["Privileges"]))
    if "Hp" in json_local_users["Oem"]:
       print("User : {} :: Privileges : {}".format(json_local_users["UserName"], json_local_users["Oem"]["Hp"]["Privileges"]))
    elif "Hpe" in json_local_users["Oem"]:
       print("User : {} :: Privileges : {}".format(json_local_users["UserName"], json_local_users["Oem"]["Hpe"]["Privileges"]))
    else:
        print("User : {} :: Privileges : {}".format(json_local_users["UserName"], json_local_users["Oem"]))
#    for items in json_local_users['Oem']:
#        print(items)
