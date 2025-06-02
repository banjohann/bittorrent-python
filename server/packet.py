import json

class DataPacket:
    def __init__(self, data, ip, port):
        self.content = json.loads(data.decode())
        self.ip = ip
        self.port = port
