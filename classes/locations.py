from classes.inventory import Item
from classes.parser import get_prep
from website_utils.utils import my_print, my_input

SENTINEL = None


# This is an obstacle. It is meant to be an item that the player can interact with but cannot pick up. E.g, a door.
class Obstacle(Item):
    def __init__(self, name, type, des, weight, breakable=False, short_des="", syns=SENTINEL, adjs=SENTINEL, verbs=SENTINEL, funcs=SENTINEL):
        super().__init__(name, type, des, weight, breakable=breakable, short_des=short_des, syns=syns, adjs=adjs)
        self.status = True
        if verbs == SENTINEL:
            self.verbs = []
        else:
            self.verbs = verbs

        if funcs == SENTINEL:
            self.funcs = {}
        else:
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
    def __init__(self, name, type, des, weight, inv, breakable=False, short_des="", syns=SENTINEL, adjs=SENTINEL, verbs=SENTINEL, funcs=SENTINEL, req_locks=[], can_remove=True):
        super().__init__(name, type, des, weight, breakable=breakable, short_des=short_des, syns=syns, adjs=adjs)
        self.inv = inv
        self.req_locks = req_locks
        self.locked = True
        self.closed = True
        if verbs == SENTINEL:
            self.verbs = []
        else:
            self.verbs = verbs

        if funcs == SENTINEL:
            self.funcs = {}
        else:
            self.funcs = funcs

        self.can_remove = can_remove
        self.classname = 'vault'
        self.closable = True


# This is a place which may contain items or obstacles and can be navigated through
class Location:
    def __init__(self, name, brief, inv, des="", n="", s="", e="", w="", ne="", nw="", se="", sw="", up="", down="", obstacles =SENTINEL, ob_messages=SENTINEL):
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

        for item in inv.item_map.values():
            item.container = self

        if obstacles == SENTINEL:
            self.obstacles = {}
        else:
            self.obstacles = obstacles

        for obstacle in self.obstacles.values():
            obstacle.container = self

        if ob_messages == SENTINEL:
            self.ob_messages = {}
        else:
            self.ob_messages = ob_messages

        self.classname = "location"

    def debug_print(self):
        print("------- " + self.name + "-------")
        print("NORTH:     ", self.n)
        print("SOUTH:     ", self.s)
        print("EAST:      ", self.e)
        print("WEST:      ", self.w)
        print("NORTHEAST: ", self.ne)
        print("NORTHWEST: ", self.nw)
        print("SOUTHEAST: ", self.se)
        print("SOUTHWEST: ", self.sw)
        print("UP:        ", self.up)
        print("DOWN:      ", self.down + "\n")
        print(self.des)
        print(self.brief + "\n")
        print("UNEXPLORED:", self.unexplored)
        print("INVENTORY:")
        for item in self.inv.item_map.values():
            print(item.name)
        print("\nOBSTACLES:")
        for obstacle in self.obstacles.values():
            print(obstacle.name)

    # Searches location inventory and each container/vault's inventories
    def remove_item(self, item):
        # Check own inventory
        if item.name in self.inv.item_map:
            self.inv.remove_item(item)
            return True

        # Check each inventory of an obstacle
        for obstacle in self.obstacles.values():
            if item.name == obstacle.name:
                if obstacle.weight > 100:
                    return False
                else:
                    self.obstacles.pop(item.name)
                    return True
            if obstacle.classname == 'vault' or obstacle.classname == 'container':
                if item.name in self.obstacles[obstacle].inv.item_map:
                    self.obstacles[obstacle].inv.remove_item(item)
                    return True
        return False

    # Searches for an obstacle which may or may not be present
    def find_obstacle(self, imp, context, item_name, item_adjs):
        # Add all possible obstacles & their contents to tmp_items
        tmp_items = []
        for key in self.obstacles:
            if item_name in self.obstacles[key].syns:
                tmp_items.append(self.obstacles[key])
            if self.obstacles[key].classname == 'container' or self.obstacles[key].classname == 'vault':
                for item in self.obstacles[key].inv.item_map.values():
                    if item_name in item.syns:
                        if not item_adjs:
                            tmp_items.append(item)
                        else:
                            for adj in item_adjs:
                                if adj in item.adjs:
                                    tmp_items.append(item)

        # Return false if nothing was found
        if len(tmp_items) == 0:
            return None
        # Return true if non-ambiguous obstacle was found
        elif len(tmp_items) == 1:
            return tmp_items[0]
        # Determine if ambiguities can be resolved
        elif len(tmp_items) > 1:
            if not item_adjs:
                msg = my_input("Which " + item_name + "? \n")
                item_adjs.append(msg)
            for curr_item in tmp_items:
                for adj in item_adjs:
                    if adj in curr_item.adjs:
                        tmp_items = [curr_item]
                        return tmp_items[0]
            # Adjectives did not determine which item to choose
            context.tmp_items = []
        return None

    # Removes an obstacle that you know to be present
    def remove_obstacle(self, obstacle):
        try:
            self.obstacles.pop(obstacle.name)
        except:
            my_print("err", "ERROR in remove_obstacle: tried to remove " + obstacle.name + " but it was nowhere to be found.")

    def print_surroundings(self):
        # Print surroundings
        my_print("title", self.brief.title())
        if self.unexplored:
            self.unexplored = False
            my_print("des", self.des)

            all_hidden = True
            for item in self.inv.item_map.values():
                if not item.hidden:
                    all_hidden = False

            if self.inv.weight > 0 and not all_hidden:
                my_print("des", "There is:")
                for object in self.inv.item_map.values():
                    if not object.hidden:
                        my_print("des", object.des)
                        if object.classname == 'container':
                            if object.inv.item_map and not object.closed:
                                my_print("des", "The " + object.type + " contains:")
                                for item in object.inv.item_map.values():
                                    if not item.hidden:
                                        prep = get_prep(item.name[0])
                                        my_print("des", prep.title() + " " + item.name)
            if self.obstacles:
                for obstacle in self.obstacles.values():
                    if obstacle.classname == 'container' and not obstacle.hidden:
                        my_print("des", obstacle.short_des)
                        if obstacle.inv.item_map:
                            my_print("des", "The " + obstacle.type + " contains:")
                            for item in obstacle.inv.item_map.values():
                                if not item.hidden:
                                    prep = get_prep(item.name[0])
                                    my_print("des", prep.title() + " " + item.name)
