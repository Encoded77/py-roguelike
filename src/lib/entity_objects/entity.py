class Entity:
    """ 
    A generic object to represent player, enemies, items, etc
    """
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    # Move the entity by a given amount
    def move(self, dx, dy):
        self.x += dx
        self.y += dy