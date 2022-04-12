def generate_finger_start(n: int, m: int, i: int) -> int:
    """Генерация стартового значения для Finger."""
    return (n + 2**i) % 2**m
