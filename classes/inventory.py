class Item:
    def __init__(self, name, des, weight):
        self.name = name
        self.des = des
        self.weight = weight


class Inventory:
    def __init__(self, capacity, items=[]):
        self.capacity = capacity
        self.weight = 0
        self.item_list = {}
        for item in items:
            self.weight += item.weight
            self.item_list.update({item.name : item})

    def add_item(self, item):
        if self.weight + item.weight > self.capacity:
            return False
        else:
            self.weight += item.weight
            self.item_list.update({item.name: item})
            return True

    def remove_item(self, item):
        if self.weight - item.weight < 0:
            return False
        else:
            self.weight -= item.weight
            self.item_list.pop(item.name)
            return True

    def contains(self, name):
        try:
            tmp = self.item_list[name]
            return True
        except:
            return False

    def get(self, name):
        return self.item_list[name]
