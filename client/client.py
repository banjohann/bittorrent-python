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
        self.peers = self.tracker.register()
        print("Registro no tracker concluído. Peers disponíveis:", len(self.peers))

        threading.Thread(target=self.p2p.serve, daemon=True).start()

        threading.Thread(target=self.periodic_update, daemon=True).start()
        threading.Thread(target=self.download_loop, daemon=True).start()
        while True:
            time.sleep(1)

    def periodic_update(self):
        while True:
            time.sleep(10)
            self.peers = self.tracker.update()
            print("Atualização enviada ao tracker.")

    def choose_rarest_piece(self, peers, my_pieces):
        piece_count = {} # {piece1: count}
        piece_owners = {} # {piece1: [peer1, peer2, ...]}

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
            my_pieces = set(self.piece_manager.list_pieces())
            rarest_piece, peer = self.choose_rarest_piece(self.peers, my_pieces)

            if rarest_piece is not None and peer is not None:
                self.p2p.request_piece(peer, rarest_piece)

            time.sleep(10)
