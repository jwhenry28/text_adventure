import random
from classes.parser import Imperative
from classes.context import Context


BLOCKED = None
obstacle_messages = \
    ['That is a terrible idea...', 'Good luck with that!', 'You\'d need actual muscles to pick that up...',
     'You throw your back out. Just kidding, but the thing won\'t budge.']


# Data structure for each verb function to contain meta info on what imperative needs to contain
class VerbFunction:
    def __init__(self, name, func, do_bool, ido_bool, do_missing="what", ido_missing="what", dont_search=[]):
        self.name = name
        self.func = func
        self.do_bool = do_bool
        self.ido_bool = ido_bool
        self.do_missing = do_missing
        self.ido_missing = ido_missing
        self.dont_search = dont_search


# Moves the player to a new location
def move_handler(imp, context):
    curr_loc = context.map[context.current_loc]

    # Make sure a direction was provided since router will not search for DO for this handler
    if not imp.noun:
        print("You'll have to say which compass direction to go in.")
        return

    direction = imp.noun[0][0]

    dir_map = {'north': curr_loc.n, 'n': curr_loc.n, 'south': curr_loc.s, 's': curr_loc.s,
               'east': curr_loc.e, 'e': curr_loc.e, 'west': curr_loc.w, 'w': curr_loc.w,
               'northeast': curr_loc.ne, 'ne': curr_loc.ne, 'northwest': curr_loc.nw, 'nw': curr_loc.nw,
               'southeast': curr_loc.se, 'se': curr_loc.se, 'southwest': curr_loc.sw, 'sw': curr_loc.sw,
               'up': curr_loc.up, 'down': curr_loc.down}

    try:
        new_loc = dir_map[direction]
    except:
        print("That's not a direction I recognise.")
        imp.print()
        return

    if new_loc == '':
        print("You can't go that way.")
    elif new_loc == BLOCKED:
        ob_message = context.map[context.current_loc].ob_messages[direction]
        print(ob_message)
    else:
        context.current_loc = new_loc
        context.map[new_loc].print_surroundings()
MoveHandler = VerbFunction("move_handler", move_handler, False, False, do_missing="where")


# Teleports a player to a specific location; building this for DEBUG only, but it might make a cool feature later on
def tp_handler(imp, context):
    try:
        new_loc = context.map[imp.noun[0][0]]
    except:
        print("I don't recognise that location.")
        return

    context.current_loc = new_loc.name
TpHandler = VerbFunction("tp_handler", tp_handler, False, False, do_missing="where")


# Adds an item to the player's inventory from the current location
def take_handler(imp, context):
    curr_loc = context.map[context.current_loc]

    for item in context.do:
        # Skip if item is in inventory (would only apply if user selected "all")
        if item.name in context.player.inv.item_map:
            continue

        # Make sure you can remove this item from the location
        if not curr_loc.inv.remove_item(item):
            if len(context.do) == 1:
                print(random.choice(obstacle_messages))
            else:
                print(item.type + ": " + random.choice(obstacle_messages))
            continue

        # Make sure the player can hold this item
        if not context.player.inv.add_item(item):
            print("You're holding too many things already!")
            curr_loc.inv.add_item(item)
            continue

        if len(context.do) == 1:
            if imp.verb == "obtain":
                print("'Obtained'. Did you really have to use that word Mr. Thesaurus?")
            else:
                print("Taken.")
        else:
            print(item.type + ": Taken.")
TakeHandler = VerbFunction("take_handler", take_handler, True, False, dont_search=['inventory'])


# Removes an item from the player's inventory
def drop_handler(imp, context):
    curr_loc = context.map[context.current_loc]

    for item in context.do:
        # Skip if item is in surroundings or obstacles (would only apply if user selected "all")
        if item.name in curr_loc.inv.item_map or item.name in curr_loc.obstacles:
            continue

        # Make sure you can remove this item from the location
        if not context.player.inv.remove_item(item):
            print("Hmm, very strange. That item weighs more than your total weight!")
            continue

        # Make sure the location can hold this item
        if not curr_loc.inv.add_item(item):
            print("There is not enough space here for that.")
            curr_loc.inv.add_item(item)
            continue

        # Drop item
        if len(context.do) == 1:
            print("Dropped.")
        else:
            print(item.type + ": Dropped.")
DropHandler = VerbFunction("drop_handler", drop_handler, True, False, dont_search=['surroundings', 'obstacles'])


def open_handler(imp, context):
    for obstacle in context.do:
        if obstacle.classname == 'obstacle':
            if not obstacle.status:
                print("The", obstacle.type.upper(), "is already open.")
            else:
                obstacle.funcs[imp.verb](context)
        else:
            print("That's not something you can open.")
OpenHandler = VerbFunction("open_handler", open_handler, True, False)


def close_handler(imp, context):
    for obstacle in context.do:
        if obstacle.status:
            print("The", obstacle.type.upper(), "is already closed.")
        else:
            obstacle.funcs[imp.verb](context)
CloseHandler = VerbFunction("close_handler", close_handler, True, False)


def inv_handler(imp, context):
    if context.player.inv.weight == 0:
        print("You are empty handed.")
    else:
        print("You are carrying:")
        for item in context.player.inv.item_map:
            print(context.player.inv.item_map[item].des)
InvHandler = VerbFunction("inv_handler", inv_handler, False, False)


verb_functions = {"go": MoveHandler, "move": MoveHandler, "run": MoveHandler, "walk": MoveHandler, "tp": TpHandler,
                  "take": TakeHandler, "get": TakeHandler, "grab": TakeHandler, "obtain": TakeHandler, "remove": TakeHandler,
                  "drop": DropHandler,
                  "open": OpenHandler,
                  "close": CloseHandler, "shut": CloseHandler, "slam": CloseHandler,
                  "inventory": InvHandler}


def route_imperative(imp, context):
    # Make sure a verb was entered
    if not imp.verb:
        print("I didn't understand that sentence.")
        return

    # Try to locate verb function w/ provided verb
    try:
        VerbFunc = verb_functions[imp.verb]
    # Exit if none is found and tell user this is not a valid verb
    except:
        print("I don't recognise that verb.")
        return

    # Need a DO?
    if VerbFunc.do_bool:
        if not imp.noun:
            imp.set_noun([input("What do you want to " + imp.verb + "?\n")])
            imp.set_nounq([])
            imp.print()
        # Find DO
        while imp.noun:
            context.find_do(imp, VerbFunc.dont_search)
            imp.remove_noun()
    # Need an IDO?

    VerbFunc.func(imp, context)

    context.refresh()
