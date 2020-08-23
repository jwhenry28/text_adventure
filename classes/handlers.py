import classes.context
from classes.parser import Imperative
from classes.context import Context


BLOCKED = None


# Data structure for each verb function to contain meta info on what imperative needs to contain
class VerbFunction:
    def __init__(self, name, func, do_bool, ido_bool, do_missing="what", ido_missing="what"):
        self.name = name
        self.func = func
        self.do_bool = do_bool
        self.ido_bool = ido_bool
        self.do_missing = do_missing
        self.ido_missing = ido_missing


# Moves the player to a new location
def move_handler(imp, context):
    curr_loc = context.map[context.current_loc]
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
    elif new_loc == BLOCKED:
        print("There is an obstacle here.")
    else:
        context.current_loc = new_loc
MoveHandler = VerbFunction("move_handler", move_handler, True, False, do_missing="where")


# Teleports a player to a specific location; building this for DEBUG only, but it might make a cool feature later on
def tp_handler(imp, context):
    try:
        new_loc = context.map[imp.noun]
    except:
        print("I don't recognise that location.")
        return

    context.current_loc = new_loc.name
TpHandler = VerbFunction("tp_handler", tp_handler, True, False, do_missing="where")


# Adds an item to the player's inventory from the current location
def take_handler(imp, context):
    curr_loc = context.map[context.current_loc]

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

        if imp.verb == "obtain":
            print("'Obtained'. Did you really have to use that word Mr. Thesaurus?")
        else:
            print("Taken.")
    else:
        print("You see no such thing.")
TakeHandler = VerbFunction("take_handler", take_handler, True, False)


# Removes an item from the player's inventory
def drop_handler(imp, context):
    curr_loc = context.map[context.current_loc]

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
DropHandler = VerbFunction("drop_handler", drop_handler, True, False)


def open_handler(imp, context):
    # Make sure there is an obstacle
    curr_loc = context.map[context.current_loc]
    if curr_loc.find_obstacle(imp, context):
        noun = curr_loc.active_ob.name
        if not curr_loc.active_ob.status:
            print("The", imp.noun.upper(), "is already open.")
        else:
            curr_loc.active_ob.funcs[imp.verb](curr_loc)
    else:
        print("You see no such thing.")
OpenHandler = VerbFunction("open_handler", open_handler, True, False)


def close_handler(imp, context):
    # Make sure there is an obstacle
    curr_loc = context.map[context.current_loc]
    if curr_loc.find_obstacle(imp.noun):
        noun = curr_loc.active_ob.name
        if curr_loc.active_ob.status:
            print("The", noun.lower(), "is already closed.")
        else:
            curr_loc.active_ob.funcs[imp.verb](curr_loc)
    else:
        print("You see no such thing.")
CloseHandler = VerbFunction("close_handler", close_handler, True, False)


verb_functions = {"go": MoveHandler, "move": MoveHandler, "run": MoveHandler, "walk": MoveHandler, "tp": TpHandler,
                  "take": TakeHandler, "get": TakeHandler, "grab": TakeHandler, "obtain": TakeHandler, "remove": TakeHandler,
                  "drop": DropHandler,
                  "open": OpenHandler,
                  "close": CloseHandler, "shut": CloseHandler, "slam": CloseHandler}


def route_imperative(imp, context):
    # Try to locate verb function w/ provided verb
    try:
        VerbFunc = verb_functions[imp.verb]
    # Exit if none is found and tell user this is not a valid verb
    except:
        print("I don't recognise that verb.")
        return

    print("Executing ", VerbFunc.name)

    # Need a DO?
    if VerbFunc.do_bool:
        print("DO BOOL is True")
        if imp.noun == '':
            print(imp.verb.lower(), VerbFunc.do_missing + "?")
        # Find DO
        direct_object = context.find_do(imp)
        if len(context.tmp_items) == 1:
            print("Found DO:", context.tmp_items[0].name)


    VerbFunc.func(imp, context)
