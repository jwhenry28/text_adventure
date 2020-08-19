from classes.parser import Imperative
from classes.context import Context


# Moves the player to a new location
def move_handler(imp, context):
    curr_loc = context.map[context.player.current_loc]
    direction = imp.noun

    if direction == 'north' or direction == 'n':
        if curr_loc.n == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.n
    elif direction == 'south' or direction == 's':
        if curr_loc.s == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.s
    elif direction == 'east' or direction == 'e':
        if curr_loc.e == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.e
    elif direction == 'west' or direction == 'w':
        if curr_loc.w == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.w
    elif direction == 'northeast' or direction == 'ne':
        if curr_loc.ne == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.ne
    elif direction == 'northwest' or direction == 'nw':
        if curr_loc.nw == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.nw
    elif direction == 'southeast' or direction == 'se':
        if curr_loc.se == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.se
    elif direction == 'southwest' or direction == 'sw':
        if curr_loc.sw == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.sw
    elif direction == 'up':
        if curr_loc.up == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.up
    elif direction == 'down':
        if curr_loc.down == '':
            print("You can't go that way!")
        else:
            context.player.current_loc = curr_loc.down
    else:
        print("That's not a direction I recognise.")


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

