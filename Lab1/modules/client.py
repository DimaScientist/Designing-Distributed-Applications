import os
import socket
import sys

from loguru import logger

from utils import show_image, save_to_grayscale


class Client:

    def __init__(self, server_port: int, host: str, chunk_size: int):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__server_port = server_port
        self.__chunk_size = chunk_size

    def send_data(self, image_path: str) -> None:
        try:
            self.__client_socket.connect((self.__host, self.__server_port))

            file = open(image_path, "rb")

            file_size = os.path.getsize(image_path)
            logger.info(f"File size on client: {file_size} bytes.")

            logger.info("Starting sending image...")

            image_data = file.read(self.__chunk_size)
            sending_size = 0
            while image_data:
                self.__client_socket.send(image_data)
                image_data = file.read(self.__chunk_size)
                sending_size += sys.getsizeof(image_data)
                logger.info(f"Progress: {sending_size} bytes ({round(sending_size / file_size * 100, 2)}%)")

            logger.info("Complete sending.")
            file.close()
        except ConnectionRefusedError as error:
            logger.error(error.__str__())
        finally:
            self.__client_socket.close()


def client_run(host: str, server_port: int, chunk_size: int) -> None:
    print("=" * 10 + f"Клиент запущен к порту: {server_port}" + "=" * 10)
    client = Client(server_port, host, chunk_size)

    while True:
        try:
            image_path: str = input("Введите путь до изображения: ")
            gray_image_path = save_to_grayscale(image_path)
            show_image(gray_image_path, "Исхдное изображение (клиент)")
            client.send_data(gray_image_path)
        except FileNotFoundError:
            print("Файл не найден, попробуйте еще.")
