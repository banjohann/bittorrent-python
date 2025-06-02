class Peer:
    def __init__(self, ip, port, pieces, tcp_port):
        self.ip = ip
        self.port = port
        self.pieces = pieces
        self.tcp_port = tcp_port

    def to_dict(self):
        return {
            'ip': self.ip,
            'port': self.tcp_port,
            'pieces': self.pieces
        }