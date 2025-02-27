import requests
from decouple import config

ADMIN_API_TOKEN = config('ADMIN_API_TOKEN')
ADMIN_USER_ID = config('ADMIN_USER_ID')
ROCKET_CHAT_URL = config('ROCKET_URL')


def get_headers(**kwargs):
    """Return headers required for Rocket.Chat API authentication."""
    if kwargs.get('admin'):
        return {
            "X-Auth-Token": ADMIN_API_TOKEN,
            "X-User-Id": ADMIN_USER_ID,
            "Content-Type": "application/json"
        }
    elif kwargs.get('user_id', None) and kwargs.get('user_token', None):
        return {
            "X-Auth-Token": kwargs.get('user_token'),
            "X-User-Id": kwargs.get('user_id'),
            "Content-Type": "application/json"
        }
    else:
        raise ValueError('No Credentials Provided.')


def create_user(name, username, email, password):
    """Create a user on Rocket.Chat."""
    url = f"{ROCKET_CHAT_URL}/api/v1/users.register"
    payload = {
        "name": name,
        "username": username,
        "email": email,
        "pass": password
    }
    response = requests.post(url, json=payload, headers=get_headers(admin=True))
    print(response.json())
    return response.json()


def send_message(room_id, message, **kwargs):
    """Send a message to a room in Rocket.Chat."""
    url = f"{ROCKET_CHAT_URL}/api/v1/chat.postMessage"
    payload = {
        "roomId": room_id,
        "text": message
    }
    user_id = kwargs.get('user_id', None)
    user_token = kwargs.get('user_token', None)
    if not user_id and not user_token:
        return {'error': 'User ID or User Token not provided.'}
    response = requests.post(url, json=payload, headers=get_headers(user_id=user_id, user_token=user_token))
    return response.json()


def get_chat_history(room_id, count=100, **kwargs):
    """
    Retrieve chat history from a room in Rocket.Chat.

    Args:
        room_id (str): The ID of the room to retrieve history from.
        count (int): Number of messages to retrieve (default is 50).

    Returns:
        dict: A dictionary containing the chat history or an error message.
    """
    user_id = kwargs.get('user_id', None)
    user_token = kwargs.get('user_token', None)
    if not user_id and not user_token:
        return {'error': 'User ID or User Token not provided.'}

    url = f"{ROCKET_CHAT_URL}/api/v1/channels.history"  # Change this for other room types
    params = {
        "roomId": room_id,
        "count": count  # Number of messages to retrieve
    }
    response = requests.get(url, params=params, headers=get_headers(user_id=user_id, user_token=user_token))
    if response.status_code == 200:
        return response.json()  # Successfully retrieved messages
    else:
        return {"error": response.json()}  # Return the error response


def login_user(username, email, password):
    url = f"{ROCKET_CHAT_URL}/api/v1/login"
    payload = {
        "user": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    data = response.json()
    # print(data)
    if data.get('status') == 'success':
        # print(data['data']['authToken'], data['data']['userId'])
        return data['data']['userId'], data['data']['authToken']
    else:
        create_user(username, username, email, password)
        return login_user(username, email, password)
