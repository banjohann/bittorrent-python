import socket
import threading
import json

class PeerConnection:
    def __init__(self, client_port, piece_manager):
        self.client_port = client_port
        self.piece_manager = piece_manager

    def request_piece(self, peer, piece_id):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((peer.ip, peer.port))
                s.sendall(json.dumps({'type': 'request', 'piece': piece_id}).encode())
                data = s.recv(4096)
                self.piece_manager.save_piece(piece_id, data)
                print(f"Recebido pedaço {piece_id} de {peer.ip}:{peer.port}")
            except Exception as e:
                print(f"Erro ao conectar com peer {peer.ip}:{peer.port} - {e}")

    def serve(self):
        def handler(conn, addr):
            data = conn.recv(4096)
            message = json.loads(data.decode())
            if message['type'] == 'request' and self.piece_manager.has_piece(message['piece']):
                piece_data = self.piece_manager.get_piece(message['piece'])
                conn.sendall(piece_data)
            else:
                conn.sendall(b"")
            conn.close()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', self.client_port))
        server.listen()
        print(f"Cliente P2P ouvindo em {self.client_port}")
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handler, args=(conn, addr)).start()