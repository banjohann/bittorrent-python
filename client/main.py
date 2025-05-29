import random
from client import Client

TRACKER_IP = '127.0.0.1'
TRACKER_PORT = 6881
CLIENT_PORT = random.randint(10000, 60000)

if __name__ == "__main__":
    client = Client(TRACKER_IP, TRACKER_PORT, CLIENT_PORT)
    client.start()