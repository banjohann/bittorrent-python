import json
from peer import Peer

class TrackerClient:
    def __init__(self, sock, tracker_ip, tracker_port, client_port, piece_manager):
        self.sock = sock
        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port
        self.client_port = client_port
        self.piece_manager = piece_manager

    def register(self):
        return self._send_and_receive('register')

    def update(self):
        return self._send_and_receive('update')

    def _send_and_receive(self, msg_type):
        message = {
            'type': msg_type,
            'port': self.client_port,
            'pieces': self.piece_manager.list_pieces()
        }

        self.sock.sendto(json.dumps(message).encode(), (self.tracker_ip, self.tracker_port))

        data, _ = self.sock.recvfrom(4096)
        peers_dict = json.loads(data.decode())['peers']

        peers = []
        for peer_dict in peers_dict:
            peer = Peer(
                peer_dict['ip'],
                peer_dict['port'],
                peer_dict['pieces']
            )
            peers.append(peer)

        return peers