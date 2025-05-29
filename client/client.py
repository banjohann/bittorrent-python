import socket
import threading
import time
import random

from piece_manager import PieceManager
from tracker_client import TrackerClient
from peer_connection import PeerConnection

class Client:
    def __init__(self, tracker_ip, tracker_port, client_port):
        self.piece_manager = PieceManager()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tracker = TrackerClient(self.sock, tracker_ip, tracker_port, client_port, self.piece_manager)
        self.p2p = PeerConnection(client_port, self.piece_manager)
        self.client_port = client_port
        self.peers = []

    def start(self):
        threading.Thread(target=self.p2p.serve, daemon=True).start()
        threading.Thread(target=self.periodic_update, daemon=True).start()
        threading.Thread(target=self.download_loop, daemon=True).start()
        while True:
            time.sleep(1)

    def periodic_update(self):
        while True:
            time.sleep(30)
            self.peers = self.tracker.update()
            print("Atualização enviada ao tracker.")

    def download_loop(self):
        while True:
            peers = self.peers
            my_pieces = set(self.piece_manager.list_pieces())
            piece_count = {}
            for peer in self.peers:
                for piece in peer['pieces']:
                    piece_count[piece] = piece_count.get(piece, 0) + 1
            rarest_pieces = sorted(piece_count, key=lambda x: piece_count[x])
            for piece in rarest_pieces:
                if piece not in my_pieces:
                    rarest_piece = piece
                    break
            else:
                rarest_piece = None

            if rarest_piece is not None:
                candidates = [peer for peer in peers if rarest_piece in peer['pieces']]
                if candidates:
                    peer = random.choice(candidates)
                    self.p2p.request_piece(peer, rarest_piece)

            for peer in peers:
                for piece in peer['pieces']:
                    if piece not in my_pieces:
                        self.p2p.request_piece(peer, piece)
            time.sleep(10)