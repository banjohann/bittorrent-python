import socket
import threading
import json

class PeerConnection:
    def __init__(self, piece_manager):
        self.piece_manager = piece_manager
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 0))
        self.client_port = self.server.getsockname()[1]
        print(f"Servidor TCP rodando na porta: {self.client_port}")

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
            try:
                data = conn.recv(4096)
                message = json.loads(data.decode())
                if message['type'] == 'request' and self.piece_manager.has_piece(message['piece']):
                    piece_data = self.piece_manager.get_piece(message['piece'])
                    conn.sendall(piece_data)
                    print(f"Enviado pedaço {message['piece']} para {addr}")
                else:
                    conn.sendall(b"")
                    print(f"Pedido inválido ou peça não encontrada de {addr}")
            except Exception as e:
                print(f"Erro ao processar pedido de {addr}: {e}")
            finally:
                conn.close()

        self.server.listen(5)
        print(f"Cliente P2P ouvindo em {self.client_port}")

        while True:
            try:
                conn, addr = self.server.accept()
                print(f"Nova conexão de {addr}")
                threading.Thread(target=handler, args=(conn, addr)).start()
            except Exception as e:
                print(f"Erro ao aceitar conexão: {e}")