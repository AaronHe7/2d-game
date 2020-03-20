from assets import *

class Gui:
    def __init__(self):
        pass
    def return_bar(self, hp):
        bar = []
        for i in range(1,11):
            if hp >= i * 2:
                bar.append(2)
            elif i < hp < i*2:
                bar.append(1)
            else:
                bar.append(0)
        return bar
