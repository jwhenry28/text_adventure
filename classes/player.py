from classes.inventory import Inventory
from classes.inventory import Item

SENTINEL = None


class Player:
    def __init__(self):
        self.name = "Wade"
        self.injured = False
        self.inv = Inventory(100)
        self.status = []


class Equipment(Item):
    def __init__(self, name, type, des, weight, breakable=False, short_des="", syns=SENTINEL, adjs=SENTINEL, traits=SENTINEL, equip_func=None):
        super().__init__(name, type, des, weight, breakable=breakable, short_des=short_des, syns=syns, adjs=adjs, traits=traits)
        self.equip_func = equip_func
        self.classname = "equipment"
