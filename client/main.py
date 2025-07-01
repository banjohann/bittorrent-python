import random
from client import Client

TRACKER_IP = '10.20.180.211'
TRACKER_PORT = 6881

if __name__ == "__main__":
    client = Client(TRACKER_IP, TRACKER_PORT)

    try:
        client.start()
    except KeyboardInterrupt:
        print("Encerrando o cliente...")
        client.logoff()