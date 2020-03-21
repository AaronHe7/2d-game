from assets import *

class Gui:
    def __init__(self):
        pass
    def return_bar(self, hp):
        bar = []
        current = 0
        for i in range(1,12):
            if hp >= current:
                bar.append(2)
            elif current - 2 < hp < current:
                bar.append(1)
            else:
                bar.append(0)
            current += 2
        bar.pop(0)
        return bar
