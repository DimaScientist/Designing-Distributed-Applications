from loguru import logger

from config import Config
from src.chord_node import ChordNode
from src.utils import stabilisation


if __name__ == "__main__":
    configuration = Config()

    logger.info(f"Создаем узлы в количестве: {configuration.NUMBER_NODE} и количество бит: {configuration.BYTE_LENGTH}")

    node_list = []
    head_node = ChordNode(0, configuration.BYTE_LENGTH)
    head_node.join(None)
    node_list.append(head_node)

    for n in range(1, configuration.NUMBER_NODE):
        chord_node = ChordNode(n, configuration.BYTE_LENGTH)
        chord_node.join_to_node(head_node)
        node_list.append(chord_node)

    logger.info("Узлы созданы")
    stabilisation(node_list)

    logger.info("Добавим узел...")
    new_node = ChordNode(configuration.NUMBER_NODE + 1, configuration.BYTE_LENGTH)
    new_node.join_to_node(head_node)
    node_list.append(new_node)
    stabilisation(node_list)
    logger.info("Узел добавлен")

    logger.info("Удаляем добавленный узел...")
    node_list.remove(new_node)
    new_node.delete()
    stabilisation(node_list)
    logger.info("Узел удален успешно")


