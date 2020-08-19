from classes.inventory import Item
from classes.inventory import Inventory


# This is a place which may contain items or obstacles and can be navigated through
class Location:
    def __init__(self, name, brief, inv, des="", n="", s="", e="", w="", ne="", nw="", se="", sw="", up="", down="", obstacles ={}, ob_funcs = {}):
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
        self.unexplored = True
        self.inv = inv
        self.obstacles = obstacles
        self.ob_funcs = ob_funcs
        self.active_ob = None

    def find_obstacle(self, noun):
        for key in self.obstacles:
            if noun in self.obstacles[key].syns:
                self.active_ob = self.obstacles[key]
                return True

        return False


# This is an obstacle. It is meant to be an item that the player can interact with but cannot pick up. E.g, a door.
class Obstacle:
    def __init__(self, name, des, verbs=[], syns=[]):
        self.name = name
        self.verbs = verbs
        self.des = des
        self.status = True
        self.syns = syns
