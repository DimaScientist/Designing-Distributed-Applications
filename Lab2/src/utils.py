from loguru import logger
from tqdm import tqdm


def generate_finger_start(n: int, m: int, i: int) -> int:
    """Генерация стартового значения для Finger."""
    return (n + 2 ** i) % 2 ** m


def log_nodes(nodes) -> None:
    """Печать узлов в качестве логов."""
    logger.debug("Узлы:")
    for node in nodes:
        logger.debug(f"{str(node)}")


def stabilisation(nodes) -> None:
    """Стабилизация узлов в списке."""
    logger.info("Стабилизируем узлы...")

    iterations = len(nodes) * len(nodes) + 1
    for i in tqdm(range(iterations)):
        for node in nodes:
            node.stabilize()
            node.fix_fingers()

    logger.info("Стабилизация окончена")

    log_nodes(nodes)
