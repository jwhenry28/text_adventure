from classes.inventory import Item
from classes.inventory import Inventory


class Player:
    def __init__(self):
        self.name = "Wade"
        self.injured = False
        self.current_loc = "cornfield south"
        self.inv = Inventory(100)