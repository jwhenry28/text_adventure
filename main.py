from classes.parser import get_imperative, regex_imperative, Imperative
from classes.locations import Location
from classes.player import Player
from classes.handlers import route_imperative
from classes.context import Context, gen_context
from classes.inventory import Item, Inventory


context = gen_context()

while True:
    # Print surroundings
    loc = context.map[context.current_loc]
    print(loc.brief.title())
    if loc.unexplored:
        print(loc.des)
        loc.unexplored = False

    if loc.inv.weight > 0:
        print("There is:")
        for key in loc.inv.item_map:
            print(loc.inv.item_map[key].name.title())

    # Gather input from player
    imp = get_imperative()
    route_imperative(imp, context)


    print("\n")
