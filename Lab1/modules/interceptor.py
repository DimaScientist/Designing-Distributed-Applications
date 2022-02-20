import os.path
import socket
import tempfile
import cv2
import shutil

from utils import salt_and_paper_noise, is_open_port


class Interceptor:

    def __init__(self, host: str, port: int, client_port: int, chunk_size: int):
        self.__host = host
        self.__port = port
        self.__client_port = client_port
        self.__chunk_size = chunk_size
        self.__interceptor_socket_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__interceptor_socket_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tmp_folder = tempfile.gettempdir()
        self.__file_path: str = ""

    def __upload_image(self) -> None:
        self.__interceptor_socket_listener.bind((self.__host, self.__client_port))
        self.__interceptor_socket_listener.listen()

        client_socket, client_address = self.__interceptor_socket_listener.accept()
        file_path = os.path.join(self.__tmp_folder, "client_image.jpg")
        file = open(file_path, "wb")
        image_chunk = client_socket.recv(self.__chunk_size)

        while image_chunk:
            file.write(image_chunk)
            image_chunk = client_socket.recv(self.__chunk_size)

        file.close()
        client_socket.close()
        self.__file_path = file_path

    def __add_noise(self) -> None:
        if len(self.__file_path) == 0:
            print("Изображение не перехвачено.")
            return
        else:
            img = cv2.imread(self.__file_path)
            self.__file_path = os.path.join(self.__tmp_folder, "noise_image.jpg")
            cv2.imwrite(self.__file_path, salt_and_paper_noise(img))

    def intercept_image(self) -> None:
        self.__upload_image()
        self.__add_noise()
        self.__interceptor_socket_sender.connect((self.__host, self.__port))
        file = open(self.__file_path, "wb")

        image_data = file.read(self.__chunk_size)
        while image_data:
            self.__interceptor_socket_sender.send(image_data)
            image_data = file.read(self.__chunk_size)

        file.close()
        self.__interceptor_socket_sender.close()
        shutil.rmtree(self.__tmp_folder, ignore_errors=True)


def interceptor_run(host: str, port: int, client_port: int, chunk_size: int) -> None:
    print("=" * 10 + f"Перехватчик запущен на порту: {port}" + "=" * 10)
    while True:
        if is_open_port(client_port, host):
            interceptor = Interceptor(host, port, client_port, chunk_size)
            interceptor.intercept_image()
