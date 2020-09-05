from nltk import word_tokenize
from classes.parser import mini_parse


class Item:
    def __init__(self, name, type, des, weight, breakable=False, short_des="", syns=[], adjs=[], traits=[]):
        self.name = name      # Name should be 100% unique
        self.type = type      # Type does not need to be unique; will likely be what player types for direct object
        self.des = des        # Description (for 'examine' verb)
        if short_des:
            self.short_des = short_des
        else:
            self.short_des = des
        self.weight = weight  # Between 1-100
        self.adjs = adjs      # Should be unique to this item within a type - two items can't share type & an adjective
        self.syns = syns      # No uniqueness required
        self.traits = traits  # Needed to determine if item can do certain types of actions
        self.breakable = breakable
        self.classname = "item"


# Containers are meant to be an item that can hold other items
class Container(Item):
    def __init__(self, name, type, des, weight, inv, breakable=False, short_des="", syns=[], adjs=[], verbs=[], funcs={}):
        super().__init__(name, type, des, weight, breakable, short_des, syns, adjs)
        self.verbs = verbs
        self.inv = inv
        self.closed = True
        self.funcs = funcs
        self.classname = "container"


class Inventory:
    def __init__(self, capacity, items=[]):
        self.capacity = capacity
        self.weight = 0
        self.item_map = {}
        if items:
            for item in items:
                self.weight += item.weight
                self.item_map.update({item.name : item})

    def print(self):
        for key in self.item_map:
            print(key + ": " + self.item_map[key].des)

    def add_item(self, item):
        if self.weight + item.weight > self.capacity:
            return False
        else:
            self.weight += item.weight
            self.item_map.update({item.name: item})
            return True

    def remove_item(self, item):
        if self.weight - item.weight < 0:
            return False
        else:
            self.weight -= item.weight
            self.item_map.pop(item.name)
            return True

    def contains(self, name):
        try:
            tmp = self.item_map[name]
            return True
        except:
            for item in self.item_map:
                for syn in self.item_map[item].syns:
                    if syn == name:
                        return True
            return False

    # Use this function when you don't know if the item is present (i.e., allocating a DO)
    def find(self, imp, context, item_name, item_adjs):
        # Add all possible items to tmp_items
        tmp_items = []
        for key in self.item_map:
            if item_name in self.item_map[key].syns:
                tmp_items.append(self.item_map[key])

        # Return false if nothing was found
        if len(tmp_items) == 0:
            return None
        # Return true if non-ambiguous obstacle was found
        elif len(tmp_items) == 1:
            return tmp_items[0]
        # Determine if ambiguities can be resolved
        elif len(tmp_items) > 1:
            if not item_adjs:
                clarification = input("Which " + item_name + "? \n")
                imp.print()
                imp =
                for word in word_tokenize(clarification):
                    item_adjs.append(word)
            for curr_item in tmp_items:
                for adj in item_adjs:
                    if adj in curr_item.adjs:
                        tmp_items = [curr_item]
                        return tmp_items[0]
            # Adjectives did not determine which item to choose
            context.tmp_items = []
        return None
