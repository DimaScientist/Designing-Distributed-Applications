import os.path
import socket
import sys
import tempfile
import uuid

import numpy as np
from PIL import Image
from loguru import logger

from utils import salt_and_paper_noise


class Interceptor:

    def __init__(self, host: str, port: int, server_port: int, chunk_size: int):
        self.__host = host
        self.__port = port
        self.__server_port = server_port
        self.__chunk_size = chunk_size
        self.__interceptor_socket_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__interceptor_socket_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tmp_folder = tempfile.gettempdir()
        self.__file_path: str = ""

    def __del__(self):
        self.__interceptor_socket_listener.close()
        self.__interceptor_socket_sender.close()

    def start_listening(self) -> None:
        logger.info(f"\nInterceptor listening on: {self.__host}:{self.__port}")
        self.__interceptor_socket_listener.bind((self.__host, self.__port))
        self.__interceptor_socket_listener.listen()

    def __upload_image(self) -> None:
        client_socket, client_address = self.__interceptor_socket_listener.accept()
        file_path = os.path.join(self.__tmp_folder, f"{uuid.uuid4()}.png")
        file = open(file_path, "wb")
        image_chunk = client_socket.recv(self.__chunk_size)

        logger.info("Starting receiving data...")

        receive_size = 0
        while image_chunk:
            file.write(image_chunk)
            receive_size += sys.getsizeof(image_chunk)
            logger.info(f"Receive data: {receive_size} bytes")
            image_chunk = client_socket.recv(self.__chunk_size)

        logger.info("Receiving data complete.")
        file.close()
        client_socket.close()
        self.__file_path = file_path

    def __add_noise(self) -> None:
        if len(self.__file_path) == 0:
            print("Изображение не перехвачено.")
            return
        else:
            result_image = salt_and_paper_noise(np.array(Image.open(self.__file_path).convert('L')))
            self.__file_path = os.path.join(self.__tmp_folder, f"{uuid.uuid4()}.png")
            Image.fromarray((result_image).astype(np.uint32)).save(self.__file_path)

    def intercept_image(self) -> None:
        self.__upload_image()
        self.__add_noise()
        self.__interceptor_socket_sender.connect((self.__host, self.__server_port))
        file = open(self.__file_path, "rb")

        file_size = os.path.getsize(self.__file_path)

        logger.info("Starting sending data...")
        image_data = file.read(self.__chunk_size)
        sending_size = 0
        while image_data:
            self.__interceptor_socket_sender.send(image_data)
            image_data = file.read(self.__chunk_size)
            sending_size += sys.getsizeof(image_data)
            logger.info(f"Progress: {sending_size} bytes ({round(sending_size / file_size * 100, 2)}%)")

        logger.info("Complete sending.")
        file.close()
        self.__interceptor_socket_sender.close()


def interceptor_run(host: str, port: int, server_port: int, chunk_size: int) -> None:
    interceptor = Interceptor(host, port, server_port, chunk_size)
    interceptor.start_listening()
    while True:
        interceptor.intercept_image()
