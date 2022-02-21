from time import sleep
from threading import Thread

from config import Config
from utils import get_port
from modules import client_run, interceptor_run, server_run


if __name__ == "__main__":
    server_port = get_port()
    interceptor_port = get_port()

    server_thread = Thread(target=server_run, args=(Config.HOST, server_port, Config.CHUNK_SIZE,))
    interceptor_thread = Thread(target=interceptor_run, args=(Config.HOST, interceptor_port, server_port, Config.CHUNK_SIZE,))
    client_thread = Thread(target=client_run, args=(Config.HOST, interceptor_port, Config.CHUNK_SIZE,))
    server_thread.start()
    sleep(1)
    interceptor_thread.start()
    sleep(1)
    client_thread.start()

