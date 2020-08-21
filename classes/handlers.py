from classes.parser import Imperative
from classes.context import Context


# Moves the player to a new location
def move_handler(imp, context):
    curr_loc = context.map[context.player.current_loc]
    direction = imp.noun

    dir_map = {'north': curr_loc.n, 'n': curr_loc.n, 'south': curr_loc.s, 's': curr_loc.s,
               'east': curr_loc.e, 'e': curr_loc.e, 'west': curr_loc.w, 'w': curr_loc.w,
               'northeast': curr_loc.ne, 'ne': curr_loc.ne, 'northwest': curr_loc.nw, 'nw': curr_loc.nw,
               'southeast': curr_loc.se, 'se': curr_loc.se, 'southwest': curr_loc.sw, 'sw': curr_loc.sw,
               'up': curr_loc.up, 'down': curr_loc.down}

    try:
        new_loc = dir_map[direction]
    except:
        print("I don't recognise that direction.")
        return

    if new_loc == '':
        print("You can't go that way.")
    else:
        context.player.current_loc = new_loc




# Adds an item to the player's inventory from the current location
def take_handler(imp, context):
    curr_loc = context.map[context.player.current_loc]

    if curr_loc.inv.contains(imp.noun):
        # Create a tmp item
        item = curr_loc.inv.get(imp.noun)

        # Make sure you can remove this item from the location
        if not curr_loc.inv.remove_item(item):
            print("You can't take that!")
            return

        # Make sure the player can hold this item
        if not context.player.inv.add_item(item):
            print("You're holding too many things already!")
            curr_loc.inv.add_item(item)
            return

        print("Taken.")
    else:
        print("You see no such thing.")


# Removes an item from the player's inventory
def drop_handler(imp, context):
    curr_loc = context.map[context.player.current_loc]
    print("dropping " + imp.noun + " in " + curr_loc.name)

    if context.player.inv.contains(imp.noun):
        # Create a tmp item
        item = context.player.inv.get(imp.noun)

        # Make sure you can remove this item from your inventory
        if not context.player.inv.remove_item(item):
            print("You can't drop that!")
            return

        # Make sure the location can hold this item
        if not curr_loc.inv.add_item(item):
            print("There are too many things here already!")
            context.player.inv.add_item(item)
            return

        print("Dropped.")
    else:
        print("You see no such thing.")


def open_handler(imp, context):
    # Make sure there is an obstacle
    curr_loc = context.map[context.player.current_loc]
    if curr_loc.find_obstacle(imp.noun):
        noun = curr_loc.active_ob.name
        curr_loc.ob_funcs[noun](curr_loc)
    else:
        print("You see no such thing.")


def route_imperative(imp, context):
    # Movement
    if imp.verb == 'go' or imp.verb == 'move' or imp.verb == 'run':
        move_handler(imp, context)
    # Taking things
    elif imp.verb == 'take' or imp.verb == 'grab' or imp.verb == 'get':
        take_handler(imp, context)
    # Dropping things
    elif imp.verb == 'drop':
        drop_handler(imp, context)
    # Opening obstacles
    elif imp.verb == 'open':
        open_handler(imp, context)

