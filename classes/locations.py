from classes.inventory import Item
from classes.inventory import Inventory


# This is an obstacle. It is meant to be an item that the player can interact with but cannot pick up. E.g, a door.
class Obstacle(Item):
    def __init__(self, name, type, des, weight, syns=[], adjs=[], verbs=[], funcs={}):
        super().__init__(name, type, des, weight, syns, adjs)
        self.verbs = verbs
        self.status = True
        self.funcs = funcs
        self.classname = "obstacle"

    def print(self):
        print("NAME   : " + self.name)
        print("DES    : ", self.des)
        print("WEIGHT : " + str(self.weight))
        print("SYNS   :", self.syns)
        print("ADJS   :", self.adjs)
        print("VERBS  :", self.verbs)
        print("STATUS :", self.status)


# This is a place which may contain items or obstacles and can be navigated through
class Location:
    def __init__(self, name, brief, inv, des="", n="", s="", e="", w="", ne="", nw="", se="", sw="", up="", down="", obstacles ={}, ob_messages={}):
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
        self.ob_messages = ob_messages

    def find_obstacle(self, imp, context):
        # Add all possible items to tmp_items
        item_name = imp.noun[0][0]
        item_adjs = imp.nounq[0]
        tmp_items = []
        for key in self.obstacles:
            if item_name in self.obstacles[key].syns:
                tmp_items.append(self.obstacles[key])

        # Return false if nothing was found
        if len(tmp_items) == 0:
            return None
        # Return true if non-ambiguous obstacle was found
        elif len(tmp_items) == 1:
            return tmp_items[0]
        # Determine if ambiguities can be resolved
        elif len(tmp_items) > 1:
            if not item_adjs:
                item_adjs.append(input("which " + item_name + "? \n"))
            for curr_item in tmp_items:
                for adj in item_adjs:
                    if adj in curr_item.adjs:
                        tmp_items = [curr_item]
                        return tmp_items[0]
            # Adjectives did not determine which item to choose
            context.tmp_items = []
        return None

    def print_surroundings(self):
        # Print surroundings
        print(self.brief.title())
        if self.unexplored:
            print(self.des)
            self.unexplored = False

        if self.inv.weight > 0:
            for key in self.inv.item_map:
                print(self.inv.item_map[key].des + " is here.")
