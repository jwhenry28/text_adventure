from classes.inventory import Item
from classes.inventory import Inventory


class Location:
    def __init__(self, name, brief, inv, des="", n="", s="", e="", w="", ne="", nw="", se="", sw="", up="", down="", doors=[]):
        self.name = name
        self.brief = brief
        self.des = des
        self.n = n
        self.s = s
        self.e = e
        self.w = w
        self.ne = ne
        self.nw = nw
        self.se = se
        self.sw = sw
        self.up = up
        self.down = down
        self.doors = doors
        self.unexplored = True
        self.inv = inv

