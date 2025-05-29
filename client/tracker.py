import json

def register_with_tracker(sock, tracker_ip, tracker_port, client_port, pieces):
    message = {
        'type': 'register',
        'port': client_port,
        'pieces': pieces
    }
    sock.sendto(json.dumps(message).encode(), (tracker_ip, tracker_port))
    data, _ = sock.recvfrom(4096)
    response = json.loads(data.decode())
    return response['peers']

def update_tracker(sock, tracker_ip, tracker_port, client_port, pieces):
    message = {
        'type': 'update',
        'port': client_port,
        'pieces': pieces
    }
    sock.sendto(json.dumps(message).encode(), (tracker_ip, tracker_port))