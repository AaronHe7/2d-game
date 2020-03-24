class Block:
    def __init__(self, id):
        self.id = id
        durabilities = [0, 5, 5, 10, 3, 15]
        self.max_durability = durabilities[id]
        self.durability = self.max_durability
        
