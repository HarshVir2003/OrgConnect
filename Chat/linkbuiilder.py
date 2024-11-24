import base64

class ChatLinkMaker:
    def __init__(self, user1, user2):
        self.lis = sorted([user1,user2])

    def make_link(self):
        word = self.lis[0] + self.lis[1]
        encoded = base64.b64encode(word.encode("utf-8"))
        encoded = encoded.decode('utf-8')
        return f"localhost:8000/" + encoded

