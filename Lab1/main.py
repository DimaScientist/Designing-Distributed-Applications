from config import Config
from utils import get_port
from modules import client_run, interceptor_run, server_run


if __name__ == "__main__":
    client_port = get_port()
    client_run(Config.HOST, client_port, Config.CHUNK_SIZE)
    interceptor_port = get_port()
    interceptor_run(Config.HOST, interceptor_port, client_port, Config.CHUNK_SIZE)
    server_port = get_port()
    server_run(Config.HOST, server_port, client_port, interceptor_port, Config.CHUNK_SIZE)
