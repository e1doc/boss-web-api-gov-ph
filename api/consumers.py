# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer


class BuildingFileUploadConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({'message': 'hello'}))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        data = json.loads(text_data)
        message = data
        print(data)
        self.send(text_data=json.dumps({'message': 'received'}))
