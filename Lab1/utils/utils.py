import random
import socket
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from config import Config


def salt_and_paper_noise(img: np.array):
    row, col = img.shape

    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)

        x_coord = random.randint(0, col - 1)

        img[y_coord][x_coord] = 255

    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
        y_coord = random.randint(0, row - 1)

        x_coord = random.randint(0, col - 1)

        img[y_coord][x_coord] = 0

    return img


def median_filter(input_image, window_size: int = 3) -> np.array:
    height, width = input_image.shape
    mask = []
    counter = window_size // 2
    out_image = np.zeros((height, width))
    for x in range(height):

        for y in range(width):

            for i in range(window_size):
                if x + i - counter < 0 or x + i - counter > height - 1:
                    for j in range(window_size):
                        mask.append(0)
                else:
                    if y + i - counter < 0 or y + counter > width - 1:
                        mask.append(0)
                    else:
                        for j in range(window_size):
                            mask.append(input_image[x + i - counter][y + j - counter])

            mask.sort()
            out_image[x][y] = mask[len(mask) // 2]
            mask = []
    return out_image


def is_open_port(port: int, host: str) -> bool:
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_connection.connect((host, port))
        socket_connection.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        socket_connection.close()


def get_port(ports: List[int] = Config.PORTS, host: str = Config.HOST) -> int:
    for port in ports:
        if not is_open_port(port, host):
            Config.PORTS.remove(port)
            return port


def show_image(file_path: str, title: str) -> None:
    plt.title = title
    plt.imshow(mpimg.imread(file_path))
    plt.show()
