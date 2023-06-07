import requests
import logging

DOMAIN = 'domain.com'  # Replace with your actual domain
PORT = 12345  # Replace with the actual port number
username = 'username' # Replace with your actual username
password = 'password' # Replace with your actual password
protocol = 'vless' # Replace with your actual protocol
flow = "xtls-rprx-vision" # Replace with your actual flow

def get_access_token(username, password):
    url = f'https://{DOMAIN}:{PORT}/api/admin/token'
    data = {
        'username': username,
        'password': password
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def get_users_list(access_token):
    url = f'https://{DOMAIN}:{PORT}/api/users'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        users_list = response.json()
        return users_list
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while retrieving users list: {e}')
        return None

def flow_select(access_token, username, protocol, flow):
    url = f'https://{DOMAIN}:{PORT}/api/user/{username}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        user_details = response.json()

        if user_details['proxies'][protocol]['flow'] != flow:

            user_details['proxies'][protocol]['flow'] = flow
            # Modify 'links' and 'subscription_url'
            user_details['links'] = []
            user_details['subscription_url'] = ""

            response = requests.put(url, json=user_details, headers=headers)
            response.raise_for_status()
            return True
        else:
            logging.error(f'flow for user {username} already is {flow}')
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while modifying user data limit: {e}')
        return False

# Configure logging settings
logging.basicConfig(filename='script_log.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

access_token = get_access_token(username, password)
if access_token:
    users_list = get_users_list(access_token)
    if users_list:
        for user in users_list['users']:
            # Modify 'flow' for vless proxies
            if 'proxies' in user and protocol in user['proxies']:
                if flow_select(access_token, user['username'], protocol, flow):
                    print(f"User {user['username']} flow updated successfully.")
                else:
                    print(f'flow for user {username} already is {flow}')
        print("All users modified successfully.")    
    else:
        print("Failed to retrieve the users list.")
else:
    print("Failed to obtain the access token.")
