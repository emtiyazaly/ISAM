import requests
import base64
import warnings
import os
import logging
import datetime as dt
import time

#export PYTHONWARNING="ignore:Unverified HTTPS request"
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


# Define the log file path
LOG_FILE = os.getcwd() + "\logs"
if not os.path.exists(LOG_FILE):
    os.makedirs(LOG_FILE)
LOG_FILE = LOG_FILE + "\\" + dt.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d %H_%M_%S') + "_message.log"


# Set up the logger
logFormatter = logging.Formatter("%(asctime)s %(levelname)s :: %(processName)s :: %(message)s")
fileHandler = logging.FileHandler("{0}".format(LOG_FILE))
fileHandler.setFormatter(logFormatter)
rootLogger = logging.getLogger()
rootLogger.addHandler(fileHandler)
rootLogger.setLevel(logging.INFO)

# Configure logging to write to a file named "app.log"
logging.basicConfig(filename=LOG_FILE, filemode="w")

# Create a logger object
logger = logging.getLogger(__name__)

# Print the log file path
logger.info("log File: " + LOG_FILE)

# User for which password is being changed
ISAMUser = "demouser"
NewPassword = "demo@2024"

# PORD & DR SERVERS
servers = {
    "PROD ISAM PS PRI": {"ip": "192.168.115.100", "username": "admin", "password": "admin"},
    "PROD ISAM PS SEC": {"ip": "192.168.115.101", "username": "admin", "password": "admin"},
    "PROD ISAM Web PRI SEC": {"ip": "192.168.115.101", "username": "admin", "password": "admin"},
    "PROD ISAM Web SEC": {"ip": "192.168.115.102", "username": "admin", "password": "admin"},
    "DR ISAM PS PRI": {"ip": "192.168.115.101", "username": "admin", "password": "admin"},
    "DR ISAM PS SEC": {"ip": "192.168.115.102", "username": "admin", "password": "admin"},
    "DR ISAM Web SEC": {"ip": "192.168.115.100", "username": "admin", "password": "admin"},
    "DR ISAM Web SEC": {"ip": "192.168.115.106", "username": "admin", "password": "admin"}
}

def create_basic_auth_header(username, password):
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    logger.info("Basic " + encoded_credentials)
    return f"Basic {encoded_credentials}"

def DeployChanges(DESTINATION_IP, Auth):
    logger.info("=== Deploy Changes Request initiated ===")
    url = f'https://' + DESTINATION_IP +'/isam/pending_changes'
    logger.info(url)
    payload = '{}'
    logger.info(payload)
    headers = {
        'Accept': 'application/json',
        'Authorization': Auth
    }
    logger.info(headers)
    
    try:
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        message = str(response) + f"DESTINATION_IP"
    except requests.exceptions.Timeout:
        logger.error("The request timed out for [" + DESTINATION_IP + "]")
        return "The request timed out for [" + DESTINATION_IP + "]"
    except requests.exceptions.HTTPError as errh:
        logger.error(errh)
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        logger.error("Error Connecting: {errc}")
        return f"Error Connecting: {errc}"
    except requests.exceptions.RequestException as err:
        logger.error("Something went wrong: {err}")
        return f"Something went wrong: {err}"
    logger.info(response)
    print(response.text)
    logger.info("=== Deploy Changes Request finished ===")

def changePassword(server_data):
    logger.info("=== Change Password Request initiated ===")
    url = f"https://{server_data['ip']}/sysaccount/users/{ISAMUser}/v1"
    logger.info(url)
    payload = '{"password":"' + NewPassword + '"}'
    logger.info(payload)
    ba_header = create_basic_auth_header(server_data['username'], server_data['password'])
    headers = {
        'Accept': 'application/json',
        'Authorization': ba_header
    }
    logger.info(headers)
    
    try:
        #response = requests.post(url, headers=headers, data=payload, timeout=1, verify=False)
        response = requests.request("PUT", url, headers=headers, data=payload, verify=False)
        logger.info("HTTP Reponse code: " + f"{response.status_code}")
        DeployChanges(server_data['ip'], ba_header)
    except requests.exceptions.Timeout:
        logger.error("The request timed out for [" + server_data['ip'] + "]")
        return "The request timed out for [" + server_data['ip'] + "]"
    except requests.exceptions.HTTPError as errh:
        logger.error(errh)
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        logger.error("Error Connecting: {errc}")
        return f"Error Connecting: {errc}"
    except requests.exceptions.RequestException as err:
        logger.error("Something went wrong: {err}")
        return f"Something went wrong: {err}"
    logger.info(response.text)
    return response.text
    logger.info("=== Change Password Request finished ===")

# Send POST requests and print responses
for server, data in servers.items():
    response_text = changePassword(data)
    print(f"[{server} : {data['ip']}] \n{response_text}")
    logger.info("[{server} : {data['ip']}] \n{response_text}")
    logger.info("\n")
