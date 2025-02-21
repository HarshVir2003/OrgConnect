import base64
import requests
from decouple import config
from Chat.roket_chat_helper import get_headers

ROCKET_CHAT_URL = config('ROCKET_URL')
class ChatLinkMaker:
    def __init__(self, user1, user2):
        self.lis = sorted([user1, user2])

    def make_link(self):
        word = self.lis[0] + self.lis[1]
        encoded = base64.b64encode(word.encode("utf-8"))
        encoded = encoded.decode('utf-8')
        url = f'{ROCKET_CHAT_URL}/api/v1/channels.create'
        payload = {'name': encoded}
        requests.post(url, json=payload, headers=get_headers(admin=True))
        return encoded


def get_room_id(room_name):
    """Fetch the roomId for a given channel name."""
    url = f"{ROCKET_CHAT_URL}/api/v1/channels.info"
    params = {"roomName": room_name}
    response = requests.get(url, headers=get_headers(admin=True), params=params)
    data = response.json()

    if data.get("success"):
        return data["channel"]["_id"]  # Return roomId
    return None
