import numpy

class Player:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    
    def test(self, number):
        print(number*2)
    
    def force(self, vector):


d = Player("Tim", 10, 10)
