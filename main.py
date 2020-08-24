from classes.parser import get_imperative, regex_imperative, Imperative
from classes.locations import Location
from classes.player import Player
from classes.handlers import route_imperative
from classes.context import Context, gen_context
from classes.inventory import Item, Inventory


context = gen_context()

class Test:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def print(self):
        print("NAME  :", self.name)
        print("VALUE :", self.value)

context.map[context.current_loc].print_surroundings()
while True:
    # # Gather input from player
    # imp = get_imperative()
    # route_imperative(imp, context)

    imp = regex_imperative()
    route_imperative(imp, context)

    print("")  # one newline
