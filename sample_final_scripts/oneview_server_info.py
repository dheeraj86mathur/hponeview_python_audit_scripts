# -*- coding: utf-8 -*-
###
###

from pprint import pprint
from hpOneView.oneview_client import OneViewClient
from hpOneView.exceptions import HPOneViewException
from config_loader import try_load_from_file

config = {
    "ip": "oneview.fqdn.com"
    "credentials": {
        "userName": "hpadmin",
        "password": "oneviewpassword"
    }
}

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
# Get list of all server hardware resources
print("Get list of all server hardware resources")
server_hardware_all = oneview_client.server_hardware.get_all()
#print( server_hardware_all )
for serv in server_hardware_all:
#    print('%s' % (serv['name'], serv['uri']))
     print(" '%s'.\t  uri = '%s'.\t '%s'" % (serv['name'], serv['uri'], serv['serverName']))

