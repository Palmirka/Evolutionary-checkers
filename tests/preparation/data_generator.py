import random
from game.constants import fields_in_use


def generate_dict(num_keys):
    def generate_keys():
        return tuple(sorted(random.sample(range(64), random.randint(4, 16))))

    def generate_values(size):
        return [random.randint(-1, 2) for _ in range(size)]

    random_dict = {}
    for _ in range(num_keys):
        key = generate_keys()
        value_length = random.randint(3, 5)  # Number of lists in the value
        value = [generate_values(len(key)) for _ in range(value_length)]
        random_dict[key] = value
    return random_dict


def generate_random_board():
    board = [0 for _ in range(64)]
    probability = random.random()
    for field in fields_in_use:
        if random.random() < probability:
            board[field] = 1
    return int(''.join(map(str, board)), 2) << 1
