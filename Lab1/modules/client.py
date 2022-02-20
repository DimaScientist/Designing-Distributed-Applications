import socket

from utils import show_image


class Client:

    def __init__(self, port: int, host: str, chunk_size: int):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__chunk_size = chunk_size

    def send_data(self, image_path: str) -> None:
        self.__client_socket.connect((self.__host, self.__port))
        file = open(image_path, "rb")

        image_data = file.read(self.__chunk_size)
        while image_data:
            self.__client_socket.send(image_data)
            image_data = file.read(self.__chunk_size)

        file.close()
        self.__client_socket.close()


def client_run(host: str, port: int, chunk_size: int) -> None:
    print("=" * 10 + f"Клиент запущен на порту: {port}" + "=" * 10)
    client = Client(port, host, chunk_size)

    while True:
        image_path: str = input("Введите путь до изображения: ")
        show_image(image_path, "Исхдное изображение (клиент)")
        client.send_data(image_path)
