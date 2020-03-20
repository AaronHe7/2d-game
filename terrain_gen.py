import random
def generate_terrain(x, y):
    return random.randint(1,4)
    if y < 0:
        return 0
    elif y == 0:
        return 1
    elif y > 0:
        return 2
