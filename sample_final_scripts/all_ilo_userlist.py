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
import openpyxl
import xlsxwriter

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
#    "ip": "oneviewqa.qasgxdo.qasgx.com",
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
#sgx_output_csv.write("Oneview Api Version : {}".format(oneview_client.api_version))
##Write all stdout to a file
sgx_output_path = "../sample_outputs/"
sgx_output_file = sgx_output_path+config['ip'].split(".")[0]+"_allILOusers"+"_"+sgx_date.strftime("%d%b%Y")+".csv"
sgx_output_csv = open(sgx_output_file,"w")
server_hardwares = oneview_client.server_hardware
server_hardware_all = oneview_client.server_hardware.get_all()
server_count = 1
sgx_output_csv.write("S.No,Server Name,User name,Privilege1,Privilege2,Privilege3,Privilege4,Privilege5,Privilege6,Privilege7,Privilege8,Privilege9,Privilege10")
sgx_output_csv.write("\n")
for serv in server_hardware_all:
    server_name = serv['name']
    server = server_hardwares.get_by_name(server_name)
#server_name = "C3G19ENC2, bay 1"
#server = server_hardwares.get_by_name(server_name)
#    print("server_name: '%s'" % (server_name))
    if server:
           try:
              remote_console_url = server.get_remote_console_url()
           except HPOneViewException as error:
#              sgx_output_csv.write(error.msg)
              sgx_output_csv.write("{}.,{},Unable to get Console URL,Server May be Powered Off/Disconnected,{}".format(server_count, server.data['serverName'], error.msg))
              sgx_output_csv.write("\n")
              server_count = (server_count + 1)
              continue
           ilo = remote_console_url['remoteConsoleUrl'].split("=")
           ilo_ip = ('https://'+ilo[1].split("&")[0])
           ilo_all_accounts_url = (ilo_ip+'/redfish/v1/AccountService/Accounts/')
           try:
              auth_token = ilo[2]
           except IndexError as error:
#              auth_token = null
              sgx_output_csv.write("{}.,{},Unable to Login on ILO,{}".format(server_count, server.data['serverName'], error))
              sgx_output_csv.write("\n")
              server_count = (server_count + 1)
              continue
#           print(" ILO: '%s'.\t ILOIP = '%s'.\t auth_token'%s'" % (ilo, ilo_ip, auth_token))
           my_headers = {'X-Auth-Token': auth_token, 'OData-Version': '4.0', 'Content-Type': 'application/json'}
           try:
              response = requests.get(ilo_all_accounts_url, headers=my_headers, verify = False)
              response.raise_for_status()
           except HPOneViewException as error:
#              sgx_output_csv.write(error.msg)
              sgx_output_csv.write("{}.,{},Unable to get Console URL,Server May be Powered Off/Disconnected,{}".format(server_count, server.data['serverName'], error.msg))
              sgx_output_csv.write("\n")
              server_count = (server_count + 1)
              continue
           json_data = response.json()
#           sgx_output_csv.write("############################################################################################")
#           sgx_output_csv.write("############################################################################################")
#           sgx_output_csv.write("{}.,{},{}".format(server_count, server.data['serverName'], json_data['Members@odata.count']))
           for members in json_data['Members']:
               ilo_sessionurl = (ilo_ip+members['@odata.id'])
               res_local_users = requests.get(ilo_sessionurl, headers=my_headers, verify = False)
               json_local_users = res_local_users.json()
               if "Hp" in json_local_users["Oem"]:
                  sgx_output_csv.write("{},{},{},{}".format(server_count, server.data['serverName'], json_local_users["UserName"], json_local_users["Oem"]["Hp"]["Privileges"]))
                  sgx_output_csv.write("\n")
                  server_count = (server_count + 1)
               elif "Hpe" in json_local_users["Oem"]:
                  sgx_output_csv.write("{},{},{},{}".format(server_count, server.data['serverName'], json_local_users["UserName"], json_local_users["Oem"]["Hpe"]["Privileges"]))
                  sgx_output_csv.write("\n")
                  server_count = (server_count + 1)
               else:
                  sgx_output_csv.write("{},{},{},{}".format(server_count, server.data['serverName'], json_local_users["UserName"], json_local_users["Oem"]))
                  sgx_output_csv.write("\n")
                  server_count = (server_count + 1)
sgx_output_csv.close()     
sgx_output_csv = open(sgx_output_file, "rt")
data = sgx_output_csv.read()
data = data.replace('{','').replace('}','')
sgx_output_csv.close()
sgx_output_csv = open(sgx_output_file, "wt")
sgx_output_csv.write(data)
sgx_output_csv.close()

#Convert CSV to xlsx file
df = pd.read_csv(sgx_output_file)
sgx_output_xlsx = sgx_output_path+config['ip'].split(".")[0]+"_allILOusers"+"_"+sgx_date.strftime("%d%b%Y")+".xlsx"
df.to_excel(sgx_output_xlsx, sheet_name = 'DATA', index = False)

#For pivot table creation, drop extra columns from data frame
df.drop(['S.No','Privilege1','Privilege2','Privilege3','Privilege4','Privilege5','Privilege6','Privilege7','Privilege8','Privilege9','Privilege10'],inplace=True,axis=1)

#Create table data frame
table = pd.pivot_table(df, index=['User name'],aggfunc={lambda x: len(x.unique())})

# Get the xlsxwriter workbook and worksheet objects.
writer =  pd.ExcelWriter(sgx_output_xlsx, mode="a", engine="openpyxl")
table.to_excel(writer, sheet_name='SUMMARY', startrow=1, header=False)
writer.save()
