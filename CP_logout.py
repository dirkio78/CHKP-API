import requests
import sys

requests.packages.urllib3.disable_warnings()

#create a function to logout the existing session
#This function will be called by other scripts to logout after script completed
def cp_logout(mds_ip, sid):

    #configure request parameters
    payload = '{}'
    url = 'https://' + mds_ip + '/web_api/logout'
    request_headers = {
    'X-chkp-sid': sid,
    'Content-Type': 'application/json',
    }

    # Attempt to make a POST request to the specified URL
    try:
        response = requests.post(url, data=payload, headers=request_headers, verify=False)
        print("logout")
        # Check if the request was successful
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors
        print(http_err)
        print(response.text)
        #exit the program
        sys.exit()

    except requests.exceptions.ConnectionError as conn_err:
        # Handle connection errors (e.g., DNS failure, refused connection)
        print(f"Connection error occurred: {conn_err}")

    except requests.exceptions.Timeout as timeout_err:
        # Handle timeout errors
        print(f"Timeout error occurred: {timeout_err}")

    except requests.exceptions.RequestException as req_err:
        # Handle any other requests exceptions (e.g., malformed URL)
        print(f"An error occurred: {req_err}")
        #exit the program
        sys.exit()