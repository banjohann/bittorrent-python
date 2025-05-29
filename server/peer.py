class Peer:
    def __init__(self, ip, port, pieces):
        self.ip = ip
        self.port = port
        self.pieces = pieces

    def to_dict(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'pieces': self.pieces
        }