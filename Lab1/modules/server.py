import os
import socket
import tempfile

from PIL import Image
import numpy as np

from utils import median_filter, show_image, is_open_port


class Server:

    def __init__(self, host: str, port: int, client_port: int, chunk_size: int):
        self.__port = port
        self.__host = host
        self.__client_port = client_port
        self.__chunk_size = chunk_size
        self.__server_socket_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tmp_folder = tempfile.gettempdir()
        self.__file_path: str = ""

    def __upload_image(self) -> None:
        self.__server_socket_listener.bind((self.__host, self.__client_port))
        self.__server_socket_listener.listen()

        client_socket, client_address = self.__server_socket_listener.accept()
        file_path = os.path.join(self.__tmp_folder, "client_image.jpg")
        file = open(file_path, "wb")
        image_chunk = client_socket.recv(self.__chunk_size)

        while image_chunk:
            file.write(image_chunk)
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
            self.__file_path = os.path.join(self.__tmp_folder, "clean_image.jpg")
            Image.fromarray((result_image * 255).astype(np.uint32)).save(self.__file_path)

    def receive_data(self) -> None:
        self.__upload_image()
        show_image(self.__file_path, "Изображение, полученное сервером")
        self.__clean_image()
        show_image(self.__file_path, "Очищенное изображение")


def server_run(host: str, port: int, client_port: int, interceptor_port: int, chunk_size: int) -> None:
    print("=" * 10 + f"Сервер запущен на порту: {port}" + "=" * 10)
    while True:
        listen_port = None
        if is_open_port(client_port, host):
            listen_port = client_port
        elif is_open_port(interceptor_port, host):
            listen_port = interceptor_port

        if listen_port:
            server = Server(host, port, listen_port, chunk_size)
            server.receive_data()
