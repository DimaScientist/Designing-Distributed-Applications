from __future__ import annotations

import random
from tabulate import tabulate
from typing import List, Optional

from src.finger import Finger


class ChordNode:
    """Реализация узла в алгоритме хорд."""

    id: int
    finger: List[Finger]

    def __init__(self, n: int, m: int):
        """
        Инициализация узла в алгоритме хорд.

        :param n: количество узлов в системе
        :param m: количество бит, используемых для генерации идентификаторов
        """
        self.id = n
        self.finger = [Finger(n, m, i, self) for i in range(0, m)]
        self.__predecessor = self

    def get_successor(self) -> ChordNode:
        """Выдает successor."""
        return self.finger[0].node

    def set_successor(self, node: ChordNode) -> None:
        """Устанавливает successor."""
        self.finger[0].node = node

    def get_predecessor(self) -> ChordNode:
        """Выдает predecessor."""
        return self.__predecessor

    def set_predecessor(self, node: Optional[ChordNode]) -> None:
        """Устанавливает predecessor."""
        self.__predecessor = node

    def find_successor(self, node_id: int) -> ChordNode:
        """Поиск successor по id."""
        node = self.find_predecessor(node_id)
        return node.get_successor()

    def find_predecessor(self, node_id: int) -> ChordNode:
        """Поиск predecessor по id."""
        node = self
        while not (self.__id_in_interval(node_id, node.id, node.get_successor().id)
                   or node_id == node.get_successor().id):
            node = node.closest_preceding_finger(node_id)
        return node

    def closest_preceding_finger(self, node_id: int) -> ChordNode:
        """Поиск ближайшего preceding finger."""
        m = len(self.finger)
        for i in range(m - 1, -1, -1):
            node: ChordNode = self.finger[i].node
            if self.__id_in_interval(node.id, self.id, node_id):
                return node
        return self

    def join(self, node: Optional[ChordNode]) -> None:
        """Добавление нового узла."""
        if node:
            self.init_finger_table(node)
            self.update_others()
        else:
            for i in range(len(self.finger)):
                self.finger[i].node = self
            self.set_predecessor(self)

    def init_finger_table(self, node: ChordNode) -> None:
        """Инициализация локальной таблицы finger."""
        self.finger[0].node = node.find_predecessor(self.finger[0].interval[0])
        successor = self.get_successor()
        self.set_predecessor(successor.get_predecessor())
        successor.set_predecessor(self)
        m = len(self.finger)
        for i in range(0, m):
            if self.__id_in_interval(self.finger[i + 1].interval[0], self.id, self.finger[i].node.id) \
                    or self.id == self.finger[i + 1].interval[0]:
                self.finger[i + 1].node = self.finger[i].node
            else:
                self.finger[i + 1].node = node.find_successor(self.finger[i + 1].interval[0])

    def update_others(self) -> None:
        """Обновление узлов, чьи таблицы finger относятся к узлу."""
        for i in range(0, len(self.finger)):
            index = (self.id - 2 ** i) % 2 ** len(self.finger)
            p = self.find_predecessor(node_id=index)
            p.update_finger_table(self, i)

    def update_finger_table(self, s: ChordNode, i: int) -> None:
        """Обновление таблицы информации об узлах."""
        if s.id == self.id or self.__id_in_interval(s.id, self.id, self.finger[i].node.id):
            self.finger[i].node = s
            p = self.get_predecessor()
            if p:
                p.update_finger_table(s, i)

    def join_to_node(self, node: Optional[ChordNode]) -> None:
        if node:
            self.set_predecessor(None)
            self.set_successor(node.find_successor(self.id))
        else:
            for finger in self.finger:
                finger.node = self
            self.set_predecessor(self)

    def stabilize(self) -> None:
        """Стабилизация системы."""
        x = self.get_successor().get_predecessor()
        if self.__id_in_interval(x.id, self.id, self.get_successor().id):
            self.set_successor(x)
        self.get_successor().notify(self)

    def notify(self, node: ChordNode) -> None:
        """Проверка на predecessor."""
        if self.get_predecessor() is None \
                or self.__id_in_interval(node.id, self.get_predecessor().id, self.id):
            self.set_predecessor(node)

    def fix_fingers(self) -> None:
        """Периодическое обновление таблицы finger."""
        i = random.randrange(len(self.finger))
        self.finger[i].node = self.find_successor(self.finger[i].interval[0])

    def __id_in_interval(self, node_id: int, start: int, end: int) -> bool:
        """Проверка, находится ли id в интервале [start, end)."""
        m = len(self.finger)
        _node_id = node_id
        _start = start
        _end = end
        if _start >= _end:
            _end += 2 ** m
            if _start > node_id:
                _node_id += 2 ** m
        return _start < _node_id < _end

    def delete(self) -> None:
        if self.get_predecessor():
            self.get_predecessor().set_successor(self.get_successor())
        self.get_successor().set_predecessor(self.get_predecessor())

        for i in range(len(self.finger)):
            j = self.id - 2 ** i
            p = self.find_predecessor(j)
            p.update_finger_table(self.get_successor(), i)

    def __str__(self):
        finger_table = [["interval", "node"], *[[finger.interval, finger.node.id] for finger in self.finger]]

        return f"\n{'=' * 20}\nid: {self.id}\nfinger_table:\n{tabulate(finger_table)}\n{'=' * 20}"
