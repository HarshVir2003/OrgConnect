import requests
from decouple import config
ADMIN_API_TOKEN = config('ADMIN_API_TOKEN')
ADMIN_USER_ID = config('ADMIN_USER_ID')
ROCKET_CHAT_URL = "http://localhost:3000"


def get_headers():
    """Return headers required for Rocket.Chat API authentication."""
    return {
        "X-Auth-Token": ADMIN_API_TOKEN,
        "X-User-Id": ADMIN_USER_ID,
        "Content-Type": "application/json"
    }


def create_user(username, email, password):
    """Create a user on Rocket.Chat."""
    url = f"{ROCKET_CHAT_URL}/api/v1/users.create"
    payload = {
        "username": username,
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return response.json()


def send_message(room_id, message):
    """Send a message to a room in Rocket.Chat."""
    url = f"{ROCKET_CHAT_URL}/api/v1/chat.postMessage"
    payload = {
        "roomId": room_id,
        "text": message
    }
    response = requests.post(url, json=payload, headers=get_headers())
    return response.json()


def get_chat_history(room_id, count=50):
    """
    Retrieve chat history from a room in Rocket.Chat.

    Args:
        room_id (str): The ID of the room to retrieve history from.
        count (int): Number of messages to retrieve (default is 50).

    Returns:
        dict: A dictionary containing the chat history or an error message.
    """
    url = f"{ROCKET_CHAT_URL}/api/v1/channels.history"  # Change this for other room types
    params = {
        "roomId": room_id,
        "count": count  # Number of messages to retrieve
    }
    response = requests.get(url, params=params, headers=get_headers())
    if response.status_code == 200:
        return response.json()  # Successfully retrieved messages
    else:
        return {"error": response.json()}  # Return the error response


