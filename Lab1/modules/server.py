import os
import shutil
import socket
import sys
import uuid

import numpy as np
from PIL import Image
from loguru import logger

from utils import median_filter, show_image


class Server:

    def __init__(self, host: str, port: int, chunk_size: int):
        self.__port = port
        self.__host = host
        self.__chunk_size = chunk_size
        self.__server_socket_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tmp_folder = "data"
        self.__file_path: str = ""
        if not os.path.exists(self.__tmp_folder):
            os.mkdir(self.__tmp_folder)

    def __del__(self):
        self.__server_socket_listener.close()
        shutil.rmtree(self.__tmp_folder, ignore_errors=True)

    def start_listening(self) -> None:
        logger.info(f"Server listening on: {self.__host}:{self.__port}")
        self.__server_socket_listener.bind((self.__host, self.__port))
        self.__server_socket_listener.listen()

    def __upload_image(self) -> None:
        client_socket, client_address = self.__server_socket_listener.accept()
        file_path = os.path.join(self.__tmp_folder, f"{uuid.uuid4()}.png")
        file = open(file_path, "wb+")
        image_chunk = client_socket.recv(self.__chunk_size)

        logger.info("Starting receiving data...")

        receive_size = 0
        while image_chunk:
            file.write(image_chunk)
            receive_size += sys.getsizeof(image_chunk)
            logger.info(f"Receive data: {receive_size} bytes")
            image_chunk = client_socket.recv(self.__chunk_size)

        file.close()
        client_socket.close()
        self.__file_path = file_path

    def __clean_image(self) -> None:
        if len(self.__file_path) == 0:
            print("Изображение не получено.")
            return
        else:
            result_image = median_filter(np.array(Image.open(self.__file_path)))
            self.__file_path = os.path.join(self.__tmp_folder, f"{uuid.uuid4()}.png")
            Image.fromarray((result_image).astype(np.uint32)).save(self.__file_path)

    def receive_data(self) -> None:
        self.__upload_image()
        show_image(self.__file_path, "Изображение, полученное сервером")
        self.__clean_image()
        show_image(self.__file_path, "Изображение, очищенное сервером")
        logger.info(f"Size of data on server: {os.path.getsize(self.__file_path)} bytes.")


def server_run(host: str, port: int, chunk_size: int) -> None:
    server = Server(host, port, chunk_size)
    server.start_listening()
    while True:
        server.receive_data()
