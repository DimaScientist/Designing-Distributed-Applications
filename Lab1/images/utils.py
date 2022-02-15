import random
import numpy as np


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


def median_filter_cpu(input_image, window_size: int = 3) -> np.array:
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
