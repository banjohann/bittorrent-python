import json
import socket
from peer import Peer

class TrackerClient:
    def __init__(self, sock, tracker_ip, tracker_port, client_port, piece_manager):
        self.sock = sock
        self.tracker_ip = tracker_ip
        self.tracker_port = tracker_port
        self.client_port = client_port
        self.piece_manager = piece_manager

    def register(self):
        message = {
            'type': 'register',
            'port': self.client_port,
            'pieces': self.piece_manager.list_pieces()
        }
        self.sock.sendto(json.dumps(message).encode(), (self.tracker_ip, self.tracker_port))
        
        data, _ = self.sock.recvfrom(65535)
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

    def update(self):
        message = {
            'type': 'update',
            'port': self.client_port,
            'pieces': self.piece_manager.list_pieces()
        }
        self.sock.sendto(json.dumps(message).encode(), (self.tracker_ip, self.tracker_port))
        
        try:
            self.sock.settimeout(5.0)
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
        except socket.timeout:
            print("Timeout ao aguardar resposta do tracker para update")
            return []
        finally:
            self.sock.settimeout(None)