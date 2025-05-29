import socket
import threading
import json

from peer import Peer
from packet import DataPacket

class TrackerServer:
    def __init__(self, ip='0.0.0.0', port=6881):
        self.TRACKER_IP = ip
        self.TRACKER_PORT = port
        # Estrutura: { (ip, port): Peer }
        self.peers = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.TRACKER_IP, self.TRACKER_PORT))
        print(f"Tracker rodando")
        
    def handle_peer_packet(self, data, addr):
        packet = DataPacket(data, addr[0], addr[1])

        if packet.content['type'] == 'register':
            self.handle_peer_connection(packet)
        elif packet.content['type'] == 'update':
            self.handle_update(packet)

    def handle_peer_connection(self, packet):
        key = (packet.ip, packet.port)
        self.peers[key] = Peer(packet.ip, packet.port, packet.content['pieces'])
        print(f"Peer registrado: {packet.ip}:{packet.port} -> {packet.content['pieces']}")

        peer_list = self.get_peers(packet.ip, packet.port)

        response = json.dumps({'peers': peer_list})
        self.sock.sendto(response.encode(), (packet.ip, packet.port))

    def handle_update(self, packet):
        key = (packet.ip, packet.port)
        self.peers[key].pieces = packet.content['pieces']

        print(f"Peer atualizado: {packet.ip}:{packet.port} -> {packet.content['pieces'].len()} pedaços")

        peer_list = self.get_peers(packet.ip, packet.port)

        response = json.dumps({'peers': peer_list})
        self.sock.sendto(response.encode(), (packet.ip, packet.port))

    def get_peers(self, exclude_ip, exclude_port):
        peer_list = [
            peer.to_dict()
            for (ip, port), peer in self.peers.items()
            if not (ip == exclude_ip and port == exclude_port)
        ]

        return peer_list

    def start(self):
        while True:
            data, addr = self.sock.recvfrom(4096)
            threading.Thread(target=self.handle_peer_packet, args=(data, addr)).start()