import socket
import threading
import time
import random
import json

from piece_manager import PieceManager
from tracker_client import TrackerClient
from peer_connection import PeerConnection

DEFAULT_LOOP_INTERVAL = 3

class Client:
    def __init__(self, tracker_ip, tracker_port):
        self.piece_manager = PieceManager()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.p2p = PeerConnection(self.piece_manager)
        self.client_port = self.p2p.client_port
        self.tracker = TrackerClient(self.sock, tracker_ip, tracker_port, self.client_port, self.piece_manager)
        self.peers = []

    def start(self):
        print("Tentando se registrar no tracker")
        self.peers = self.tracker.register()
        print("Registro no tracker concluído. Peers disponíveis:", len(self.peers))

        self.request_rarest_piece()
        self.request_random_piece()

        threading.Thread(target=self.p2p.serve, daemon=True).start()
        threading.Thread(target=self.periodic_update, daemon=True).start()
        threading.Thread(target=self.download_loop, daemon=True).start()

        while True:
            time.sleep(1)

    def logoff(self):
        message = {
            'type': 'logoff',
            'port': self.client_port,
        }
        self.sock.sendto(json.dumps(message).encode(), (self.tracker.tracker_ip, self.tracker.tracker_port))
        self.sock.close()

    def request_random_piece(self):
        my_pieces = set(self.piece_manager.list_pieces())
        peer = random.choice(self.peers)

        available_pieces = [piece for piece in peer.pieces if piece not in my_pieces]

        if not available_pieces:
            return

        random_piece = random.choice(available_pieces)
        self.p2p.request_piece(peer, random_piece)

    def request_rarest_piece(self):
        my_pieces = set(self.piece_manager.list_pieces())
        rarest_piece, peer = self.choose_rarest_piece(self.peers, my_pieces)

        if rarest_piece is not None and peer is not None:
            self.p2p.request_piece(peer, rarest_piece)

    def periodic_update(self):
        while True:
            time.sleep(DEFAULT_LOOP_INTERVAL)
            self.peers = self.tracker.update()
            print("Atualização enviada ao tracker.")

    def choose_rarest_piece(self, peers, my_pieces):
        piece_count = {}
        piece_owners = {}

        for peer in peers:
            for piece in peer.pieces:

                if piece in my_pieces:
                    continue

                piece_count[piece] = piece_count.get(piece, 0) + 1

                if piece not in piece_owners:
                    piece_owners[piece] = []
                piece_owners[piece].append(peer)

        rarest_pieces = sorted(piece_count.keys(), key=lambda x: piece_count[x])

        if not rarest_pieces:
            return None, None

        piece = rarest_pieces[0]
        chosen_peer = random.choice(piece_owners[piece])
        return piece, chosen_peer

    def download_loop(self):
        while True:
            self.request_rarest_piece()
            time.sleep(DEFAULT_LOOP_INTERVAL)
