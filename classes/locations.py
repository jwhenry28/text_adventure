from classes.inventory import Item
from classes.inventory import Inventory


# This is an obstacle. It is meant to be an item that the player can interact with but cannot pick up. E.g, a door.
class Obstacle(Item):
    def __init__(self, name, type, des, weight, breakable=False, short_des="", syns=[], adjs=[], verbs=[], funcs={}):
        super().__init__(name, type, des, weight, breakable, short_des, syns, adjs)
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


# Vault is a hybrid of an obstacle and a container - it can hold specific things, but also may act as a barrier
class Vault(Item):
    def __init__(self, name, type, des, weight, inv, breakable=False, short_des="", syns=[], adjs=[], verbs=[], funcs={}, req_locks=[], can_remove=True):
        super().__init__(name, type, des, weight, breakable, short_des, syns, adjs)
        self.verbs = verbs
        self.inv = inv
        self.req_locks = req_locks
        self.locked = True
        self.closed = True
        self.funcs = funcs
        self.can_remove = can_remove
        self.classname = 'vault'


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

    # Searches location inventory and each container/vault's inventories
    def remove_item(self, item):
        # Check own inventory
        if item.name in self.inv.item_map:
            self.inv.remove_item(item)
            return True
        # Check each inventory of an obstacle
        for obstacle in self.obstacles:
            if item.name in self.obstacles[obstacle].inv.item_map:
                self.obstacles[obstacle].inv.remove_item(item)
                return True
        return False

    def find_obstacle(self, imp, context, item_name, item_adjs):
        # Add all possible items to tmp_items
        tmp_items = []
        for key in self.obstacles:
            if item_name in self.obstacles[key].syns:
                tmp_items.append(self.obstacles[key])
            if self.obstacles[key].classname == 'container' or self.obstacles[key].classname == 'vault':
                for item in self.obstacles[key].inv.item_map:
                    if item_name in self.obstacles[key].inv.item_map[item].syns:
                        tmp_items.append(self.obstacles[key].inv.item_map[item])

        # Return false if nothing was found
        if len(tmp_items) == 0:
            return None
        # Return true if non-ambiguous obstacle was found
        elif len(tmp_items) == 1:
            return tmp_items[0]
        # Determine if ambiguities can be resolved
        elif len(tmp_items) > 1:
            if not item_adjs:
                item_adjs.append(input("Which " + item_name + "? \n"))
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
            self.unexplored = False
            print(self.des)

            if self.inv.weight > 0 or self.obstacles:
                print("There is:")
                for key in self.inv.item_map:
                    print(self.inv.item_map[key].des)
                for obstacle in self.obstacles.values():
                    print(obstacle.short_des)
                    if (obstacle.classname == 'container' or obstacle.classname == 'vault') and obstacle.inv.item_map:
                        print("The " + obstacle.type + " contains:")
                        for item in obstacle.inv.item_map.values():
                            if item.name[0] in ['a', 'e', 'i', 'o', 'u']:
                                prep = 'An'
                            else:
                                prep = 'A'
                            print(prep + " " + item.name)
