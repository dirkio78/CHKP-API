# This script will show output for a API call

import requests
import json
#import sys
from CP_auth_no_domain import get_auth_sid
from CP_logout import cp_logout
import pandas as pd
import os
import urllib3
import getpass
requests.packages.urllib3.disable_warnings()

#Store user 'username'
#args_username = input("Enter your username: ")
args_username = "admin"

#Use getpass function to hide user response when they Enter password
args_password = getpass.getpass(prompt="Enter your password: ")
#args_password = "hsbc1234"

#Provide a menu option to select the MDS IP
def select_mds_ip():
    mds_ips = {
        "1": "192.168.56.10",
        "2": "1.1.1.1",
        "3": "2.2.2.2", }
      
    print("Select the MDS IP address:")
    for option, ip_address in mds_ips.items():
        print(f"{option}. {ip_address}")
        
    while True:
        selection = input("Enter your choice (1-3): ").strip()
        
        if selection in mds_ips:
            return mds_ips[selection]
            
        print("Invalid selection. Please choose 1, 2, or 3.")


# Assign the selected address to mds_ip
mds_ip = select_mds_ip()
api_command = "show-api-versions"
variable_name = "5edcccd6-09b4-4892-8d53-c29da0f7e3d9"

# Check command
def check_api():
    print("Checking API command: " + api_command)
    #Use the 'get_token' function to create the authentication token variable. Need to pass MDS IP, username, password and domain as an argument
    sid = get_auth_sid(mds_ip, args_username, args_password)
    print("got the sid ok")
    # Check Point web_api commands usually require a valid JSON body.
    # An empty payload ({}) is rejected by many commands, including show-automatic-purge.
    payload = {
        "details-level": "full",
        "limit": 500,
    }
    url = f"https://{mds_ip}/web_api/{api_command}"
    print("SID is")
    print(sid)
    request_headers = {
        'X-chkp-sid': sid,
        'Content-Type': 'application/json',
    }

    printable_headers = {**request_headers, 'X-chkp-sid': '<redacted>'}
    print("executing request")
    print("HTTP POST request:")
    print(f"URL: {url}")
    print(f"Headers: {printable_headers}")
    print(f"Payload: {payload}")

    # Use json=... so Requests serializes the body correctly and sets the JSON content type.
    response = requests.post(url, json=payload, headers=request_headers, verify=False, timeout=30)

    print(response.status_code)
    print(response.text)

    if response.status_code >= 400:
        print("Request failed. Check the command name and required fields for this Check Point API version.")


    #Call the "cp_logout" funtion to logout
    cp_logout(mds_ip, sid)


#get_gateway_details("10.204.7.30", args_username, args_password, version)
check_api()