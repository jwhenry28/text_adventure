from classes.inventory import Item
from classes.inventory import Inventory


# This is a place which may contain items or obstacles and can be navigated through
class Location:
    def __init__(self, name, brief, inv, des="", n="", s="", e="", w="", ne="", nw="", se="", sw="", up="", down="", obstacles ={}):
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

    def find_obstacle(self, imp, context):
        # Reset tmp_items
        context.tmp_items = []
        for key in self.obstacles:
            if imp.noun in self.obstacles[key].syns:
                context.tmp_items.append(self.obstacles[key])

        # Return false if nothing was found
        if len(context.tmp_items) == 0:
            return False
        # Return true if non-ambiguous obstacle was found
        elif len(context.tmp_items) == 1:
            return True
        # Determine if ambiguities can be resolved
        elif len(context.tmp_items) > 1:
            adj = input("which " + imp.noun + "?")
            for obstacle in context.tmp_items:
                if adj in obstacle.syns:
                    context.tmp_items = [obstacle]
                    return True
            context.tmp_items = []
            print("You see no such thing")
        return False


# This is an obstacle. It is meant to be an item that the player can interact with but cannot pick up. E.g, a door.
class Obstacle(Item):
    def __init__(self, name, des, weight, syns=[], adjs=[], verbs=[], funcs={}):
        super().__init__(name, des, weight, syns, adjs)
        self.verbs = verbs
        self.status = True
        self.funcs = funcs
