import random
def generate_terrain(x, y, cell):
    """if cell[6] == 1 or cell[6] == 4:
        if y > -5:
            return 4
    """
    if y < 0:
        return 0
    elif y == 0:
        return 1
    elif y == 5:
        return random.choice((2,5))
    elif y > 5:
        return 5
    elif y > 0:
        return 2
