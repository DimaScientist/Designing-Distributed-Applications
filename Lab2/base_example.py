from loguru import logger

from src.chord_node import ChordNode
from src.utils import stabilisation

if __name__ == "__main__":
    logger.info("Пример из методички:")
    m = 3

    node_list = []
    head_node = ChordNode(0, m)
    head_node.join(None)
    node_list.append(head_node)

    for i in [1, 3]:
        chord_node = ChordNode(i, m)
        chord_node.join_to_node(head_node)
        node_list.append(chord_node)

    logger.info("Узлы созданы")
    stabilisation(node_list)

    logger.info("Добавим узел...")
    new_node = ChordNode(6, m)
    new_node.join_to_node(head_node)
    node_list.append(new_node)
    stabilisation(node_list)
    logger.info("Узел добавлен")

    logger.info("Удаляем добавленный узел...")
    node_list.remove(new_node)
    new_node.delete()
    stabilisation(node_list)
    logger.info("Узел удален успешно")
