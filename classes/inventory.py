class Item:
    def __init__(self, name, type, des, weight, syns=[], adjs=[]):
        self.name = name # Name should be unique
        self.type = type # Type is likely what the player will type for the direct object
        self.des = des # Brief description (for examine verb)
        self.weight = weight
        self.adjs = adjs
        self.syns = syns


class Inventory:
    def __init__(self, capacity, items=[]):
        self.capacity = capacity
        self.weight = 0
        self.item_map = {}
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

    def get(self, name):
        try:
            return self.item_map[name]
        except:
            for item in self.item_map:
                for syn in self.item_map[item].syns:
                    if syn == name:
                        return self.item_map[item]
