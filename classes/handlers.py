import random
from classes.parser import get_prep, mini_parse
from classes.context import iron_boots
from website_utils.utils import my_print, my_input


BLOCKED = None
SENTINEL = None
obstacle_messages = \
    ['That is a terrible idea.', 'Good luck with that!', 'You\'d need actual muscles to pick that up...',
     'You throw your back out. Just kidding, but the thing won\'t budge.']


# Data structure for each verb function to contain meta info on what imperative needs to contain
class VerbFunction:
    def __init__(self, name, func, do_bool, ido_bool, do_missing="What", ido_missing="What", dont_search=SENTINEL):
        self.name = name
        self.func = func
        self.do_bool = do_bool
        self.ido_bool = ido_bool
        self.do_missing = do_missing
        self.ido_missing = ido_missing
        if dont_search == SENTINEL:
            self.dont_search = []
        else:
            self.dont_search = dont_search


# Moves the player to a new location
def move_handler(imp, context):
    curr_loc = context.map[context.current_loc]

    # Make sure a direction was provided since router will not search for DO for this handler
    if not imp.noun:
        my_print("des", "You'll have to say which compass direction to go in.")
        return

    direction = imp.noun[0][0]

    full_map = {'north': 'north', 'n': 'north', 'south': 'south', 's': 'south',
                'east': 'east', 'e': 'east', 'west': 'west', 'w': 'west',
                'northeast': 'northeast', 'ne': 'northeast', 'northwest': 'northwest', 'nw': 'northwest',
                'southeast': 'southeast', 'se': 'southeast', 'southwest': 'southwest', 'sw': 'southwest',
                'up': 'up', 'u': 'up', 'd': 'down', 'down': 'down'}

    dir_map = {'north': curr_loc.n, 'n': curr_loc.n, 'south': curr_loc.s, 's': curr_loc.s,
               'east': curr_loc.e, 'e': curr_loc.e, 'west': curr_loc.w, 'w': curr_loc.w,
               'northeast': curr_loc.ne, 'ne': curr_loc.ne, 'northwest': curr_loc.nw, 'nw': curr_loc.nw,
               'southeast': curr_loc.se, 'se': curr_loc.se, 'southwest': curr_loc.sw, 'sw': curr_loc.sw,
               'up': curr_loc.up, 'down': curr_loc.down}

    try:
        full_direction = full_map[direction]
        new_loc = dir_map[full_direction]
    except:
        my_print("des", "That's not a direction I recognise.")
        return

    if new_loc == '':
        my_print("des", "You can't go that way.")
    elif new_loc == BLOCKED:
        ob_message = context.map[context.current_loc].ob_messages[full_direction]
        my_print("des", ob_message)
    else:
        context.current_loc = new_loc
        context.map[new_loc].print_surroundings()
MoveHandler = VerbFunction("move_handler", move_handler, False, False, do_missing="Where")


# Teleports a player to a specific location; building this for DEBUG only, but it might make a cool feature later on
def tp_handler(imp, context):
    try:
        new_loc = context.map[imp.noun[0][0]]
    except:
        my_print("des", "I don't recognise that location.")
        return

    context.current_loc = new_loc.name
    context.map[new_loc.name].print_surroundings()
TpHandler = VerbFunction("tp_handler", tp_handler, False, False, do_missing="Where")


# Equips an item to a player
def equip_handler(imp, context):

    curr_loc = context.map[context.current_loc]

    for item in context.do:
        # Notify player if not equipment
        if item.classname != "equipment":
            if len(context.do) == 1:
                my_print("des", "That's not something you can equip.")
            else:
                my_print("des", item.type + ": That's not something you can equip.")

        else:
            if item.name not in context.player.inv.item_map:
                if not context.player.inv.add_item(item):
                    my_print("des", "You're holding too many things already!")
                    curr_loc.inv.add_item(item)
                    continue
                else:
                    my_print("des", "(first taking the " + item.name + ")")

            item.equip_func(imp, context)
            if len(context.do) == 1:
                my_print("des", "Equipped.")
            else:
                my_print("des", item.type + ": Equipped.")
EquipHandler = VerbFunction("equip_handler", equip_handler, True, False)


# Adds an item to the player's inventory from the current location
def take_handler(imp, context):
    curr_loc = context.map[context.current_loc]
    for item in context.do:
        # Skip if item is in inventory (would only apply if user selected "all")
        if item.name in context.player.inv.item_map:
            continue

        # Make sure you can remove this item from the location
        if not curr_loc.remove_item(item, context.player):
            if len(context.do) == 1:
                my_print("des", random.choice(obstacle_messages))
            else:
                my_print("des", item.type + ": " + random.choice(obstacle_messages))
            continue

        # Make sure the player can hold this item
        if not context.player.inv.add_item(item):
            my_print("des", "You're holding too many things already!")
            curr_loc.inv.add_item(item)
            continue

        if len(context.do) == 1:
            if imp.verb == "obtain":
                my_print("des", "'Obtained'. Did you really have to use that word Mr. Thesaurus?")
            else:
                my_print("des", "Taken.")
        else:
            my_print("des", item.type + ": Taken.")

        if "taken" not in item.traits:
            item.traits.append("taken")
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
            my_print("err", "drop_handler: tried to remove item, but it weighed more than the player's weight")
            continue

        # Make sure the location can hold this item
        if not curr_loc.inv.add_item(item):
            my_print("des", "There is not enough space here for that.")
            curr_loc.inv.add_item(item)
            continue

        # Drop item
        if len(context.do) == 1:
            my_print("des", "Dropped.")
        else:
            my_print("des", item.type + ": Dropped.")

        item.traits.remove("taken")
DropHandler = VerbFunction("drop_handler", drop_handler, True, False, dont_search=['surroundings', 'obstacles'])


def open_handler(imp, context):
    for obstacle in context.do:
        if obstacle.classname == 'obstacle':
            if not obstacle.status:
                my_print("des", "The " + obstacle.type + " is already open.")
            else:
                obstacle.funcs[imp.verb](imp, context)
        elif obstacle.classname == 'container' or obstacle.classname == 'vault':
            if not obstacle.closed:
                my_print("des", "The " + obstacle.type + " is already open.")
            else:
                obstacle.funcs[imp.verb](imp, context)
        else:
            my_print("des", "That's not something you can open.")
OpenHandler = VerbFunction("open_handler", open_handler, True, False)


def close_handler(imp, context):
    for obstacle in context.do:
        if obstacle.classname == 'obstacle':
            if obstacle.status:
                my_print("des", "The", obstacle.type, "is already closed.")
            else:
                obstacle.funcs[imp.verb](imp, context)
        elif obstacle.classname == 'container' or obstacle.classname == 'vault':
            if obstacle.closed:
                my_print("des", "The " + obstacle.type + " is already closed.")
            else:
                obstacle.funcs[imp.verb](imp, context)
        else:
            my_print("des", "That's not something you can close.")
CloseHandler = VerbFunction("close_handler", close_handler, True, False)


def put_handler(imp, context):
    # You cannot split an item
    if len(context.ido) > 1:
        my_print("des", "You can't use multiple objects with that verb.")
        return

    object = context.do[0]
    container = context.ido[0]

    # Make sure player didn't try to put an item inside of itself
    if object.name == container.name:
        my_print("des", "There are two types of people in this world: Those who don't believe in infinite recursion and those that believe 'There are two types of people in this world...'")
        return

    # Make sure the IDO is actually a container
    if container.classname == 'vault':
        imp.set_verb("insert")
        container.funcs[imp.verb](imp, context)
        return
    if container.classname != 'container':
        my_print("des", "That can't contain things.")
        return

    # Move item out of inventory and into container
    if not container.inv.add_item(object):
        my_print("des", "The " + container.name + " is already full.")
        return

    if not context.player.inv.remove_item(object):
        my_print("des", "ERROR: Laws of physics have been broken. Or maybe somebody's code just isn't calculating correctly...")
        return

    return
PutHandler = VerbFunction("put_handler", put_handler, True, True, ido_missing="Where")


def inv_handler(imp, context):
    if context.player.inv.weight == 0:
        my_print("des", "You are empty handed.")
    else:
        my_print("des", "You are carrying:")
        for item in context.player.inv.item_map:
            my_print("des", context.player.inv.item_map[item].des)
InvHandler = VerbFunction("inv_handler", inv_handler, False, False)


def look_handler(imp, context):
    context.map[context.current_loc].unexplored = True
    context.map[context.current_loc].print_surroundings()
LookHandler = VerbFunction("look_handler", look_handler, False, False)


def break_handler(imp, context):
    imp.set_verb('break')
    breaker = context.ido[0]
    for object in context.do:
        # Make sure DO is breakable
        if not object.breakable:
            my_print("des", "Trying to break a " + object.name + " is not notably useful.")
            return

        # Make sure IDO is a breaker
        if 'break' not in breaker.traits:
            prep = get_prep(breaker.name)
            my_print("des", prep.title() + " " + breaker.name + " cannot be used to break things.")
            return

        # Add IDO to inventory if it is not already
        if breaker.name not in context.player.inv.item_map:
            my_print("des", "(first taking the " + breaker.name + ")")
            context.map[context.current_loc].inv.remove_item(breaker)
            context.player.inv.add_item(breaker)

        object.funcs[imp.verb](imp, context)
BreakHandler = VerbFunction("break_handler", break_handler, True, True)


# def read_handler(imp, context):
#     for page in context.do:



verb_functions = {"go": MoveHandler, "move": MoveHandler, "run": MoveHandler, "walk": MoveHandler, "tp": TpHandler,
                  "take": TakeHandler, "get": TakeHandler, "grab": TakeHandler, "obtain": TakeHandler, "remove": TakeHandler,
                  "drop": DropHandler,
                  "open": OpenHandler,
                  "close": CloseHandler, "shut": CloseHandler, "slam": CloseHandler,
                  "inventory": InvHandler,
                  "put": PutHandler, "place": PutHandler, "insert": PutHandler,
                  "look": LookHandler, "observe": LookHandler,
                  "break": BreakHandler, "destroy": BreakHandler, "chop": BreakHandler,
                  "equip": EquipHandler}


def route_imperative(imp, context):
    # Make sure a verb was entered
    if not imp.verb:
        my_print("des", "I didn't understand that sentence.")
        return

    # Try to locate verb function w/ provided verb
    try:
        VerbFunc = verb_functions[imp.verb]
    # Exit if none is found and tell user this is not a valid verb
    except:
        my_print("des", "I don't recognise that verb.")
        return

    # Need a DO?
    if VerbFunc.do_bool:
        if not imp.noun:
            clarification = my_input("What do you want to " + imp.verb + "?\n")
            imp = mini_parse(imp, clarification, context.mode)

        # Find DO
        while imp.noun:
            context.find_object(imp, VerbFunc.dont_search, context.mode)
            imp.remove_noun()

    # If no DO was found and you need one, you must exit
    if not context.do and VerbFunc.do_bool:
        context.refresh
        return

    context.toggle_mode()

    # Need an IDO?
    if VerbFunc.ido_bool:
        if not imp.second:
            msg = "What do you want to " + imp.verb
            if VerbFunc.ido_missing == "Where":
                msg = msg + " the " + context.do[0].type + " in?"
            else:
                msg = msg + " the " + context.do[0].type + " with?"
            msg += "\n"
            clarification = my_input(msg)
            imp = mini_parse(imp, clarification, context.mode)

        # Find IDO
        while imp.second:
            context.find_object(imp, VerbFunc.dont_search, context.mode)
            imp.remove_second()

    VerbFunc.func(imp, context)

    context.refresh()
