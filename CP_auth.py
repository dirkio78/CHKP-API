import requests
import sys

requests.packages.urllib3.disable_warnings()

# create a function to get the token required for future API requests. Need to pass MDS that hosts the domain, username and password when called
# This function will be called by other scripts to generate the token for authentication
def get_auth_sid(mds_ip, user, password, domain):
    
    # create global object to store SID
    global sid
    
    # configure request parameters
    payload = '{"user": "' + user + '", "password": "' + password + '", "domain": "' + domain + '"}'
    url = 'https://' + mds_ip + '/web_api/login'
    request_headers = {'Content-Type': 'application/json'}
    
    # Attempt to make a POST request to the specified URL
    try:
        response = requests.post(url, data=payload, headers=request_headers, verify=False)
        
        # Check if the request was successful
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
        
        # Extract the SID details from the auth_data variable
        auth_data = response.json()
        
        # capture the sid variable
        sid = auth_data['sid']

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors
        print(http_err)
        print(response.text)
        
        # exit the program
        sys.exit()

    except requests.exceptions.ConnectionError as conn_err:
        # Handle connection errors (e.g., DNS failure, refused connection)
        print(f"Connection error occurred: {conn_err}")
        
        # exit the program and use the 'sid' variable to capture there was a connection error
        #sys.exit()
        sid = "connection_error"
        return sid

    except requests.exceptions.Timeout as timeout_err:
        # Handle timeout errors
        print(f"Timeout error occurred: {timeout_err}")
        
        # exit the program and use the 'sid' variable to capture there was a connection error
        #sys.exit()
        sid = "connection_error"
        return sid

    except requests.exceptions.RequestException as req_err:
        # Handle any other requests exceptions (e.g., malformed URL)
        print(f"An error occurred: {req_err}")
        
        # exit the program
        sys.exit()

        # Retain sid variable to be used by other functions
        return sid