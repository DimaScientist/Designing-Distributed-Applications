from __future__ import annotations

from typing import Tuple

from src.utils import generate_finger_start


class Finger:
    """"Класс для хранения вспомогательной информации об узлах."""

    interval: Tuple[int, int]  # interval[0] - start, interval[1] - end
    node = None

    def __init__(self, n: int, m: int, i: int, node):
        """
        Инициализациия ифнормации об узлах.

        :param n: количество узлов
        :param m: количество бит, используемых для генерации идентификаторов
        :param i: индекс входа
        :param node: узел
        """
        self.__start = generate_finger_start(n, m, i)
        self.__end = generate_finger_start(n, m, i + 1)
        self.interval = (self.__start, self.__end)
        self.node = node
