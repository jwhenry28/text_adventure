from classes.parser import get_imperative, Imperative
from classes.locations import Location
from classes.player import Player
from classes.handlers import route_imperative
from classes.context import Context, gen_context
from classes.inventory import Item, Inventory


context = gen_context()

while True:
    # Print surroundings
    loc = context.map[context.player.current_loc]
    print(loc.brief.title())
    if loc.unexplored:
        print(loc.des)
        loc.unexplored = False

    if loc.inv.weight > 0:
        print("There is:")
        for key in loc.inv.item_list:
            print(loc.inv.item_list[key].name.title())

    # Gather input from player
    imp = get_imperative()
    route_imperative(imp, context)

    # inp = input("> ").lower()
    # try:
    #     loc = map[inp]
    #     player.current_loc = loc
    # except Exception as e:
    #     continue
    #
    # print(player.current_loc.des)

    print("\n")
