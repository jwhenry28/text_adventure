import random, time
from classes.parser import get_prep, mini_parse
from website_utils.utils import my_print, my_input, server_context


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
                'northeast': 'northeast', 'ne': 'northeast', 'north east': 'northeast',
                'northwest': 'northwest', 'nw': 'northwest', 'north west': 'northwest',
                'southeast': 'southeast', 'se': 'southeast', 'south east': 'southeast',
                'southwest': 'southwest', 'sw': 'southwest', 'south west': 'southwest',
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
        if 'heavy' in context.player.status:
            my_print("des", "You struggle to move with the heavy load...")
            if context.type == "server":
                server_context.html_barrier.wait()
            time.sleep(1)

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
            # Make sure item isn't already equipped
            if "equipped" in item.traits:
                my_print("des", "That item is already equipped.")
                continue

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
            item.traits.append("equipped")
            item.container = context.player
EquipHandler = VerbFunction("equip_handler", equip_handler, True, False)


# Dequips an item from player
def dequip_handler(imp, context):
    curr_loc = context.map[context.current_loc]

    for item in context.do:
        # Notify player if not equipment
        if item.classname != "equipment":
            if len(context.do) == 1:
                my_print("des", "That's not something you can de-equip.")
            else:
                my_print("des", item.type + ": That's not something you can de-equip.")

        # Notify player if not equipped or not held
        elif "equipped" not in item.traits:
            my_print("des", "That isn't currently equipped.")

        # De-equip item
        else:
            item.equip_func(imp, context)
            if len(context.do) == 1:
                my_print("des", "De-equipped.")
            else:
                my_print("des", item.type + ": De-equipped.")
            item.traits.remove("equipped")
DequipHandler = VerbFunction("dequip_handler", dequip_handler, True, False)


# Adds an item to the player's inventory from the current location
def take_handler(imp, context):
    curr_loc = context.map[context.current_loc]

    for item in context.do:
        # Define premessage
        if len(context.do) == 1:
            premessage = ""
        else:
            premessage = item.type + ": "

        # Skip if item is in inventory (would only apply if user selected "all")
        if item.name in context.player.inv.item_map:
            if not context.all:
                my_print("des", premessage + "You're holding that already.")
            continue

        # Skip if item is a liquid
        if "liquid" in item.traits:
            my_print("des", premessage + "You should find something to put that in.")
            continue

        # Make sure you can remove this item from the location
        if item.container.classname == "location":
            if not curr_loc.remove_item(item):
                my_print("des", premessage + random.choice(obstacle_messages))
                continue
        else:
            if not item.container.inv.remove_item(item):
                my_print("err", "Tried to remove", item.name, "from", item.container.name, "but failed.")
                return

        # Make sure the player can hold this item
        if not context.player.inv.add_item(item):
            my_print("des", premessage + "You're holding too many things already!")
            curr_loc.inv.add_item(item)
            continue

        if imp.verb == "obtain":
            my_print("des", premessage + "'Obtained'. Did you really have to use that word Mr. Thesaurus?")
        else:
            my_print("des", premessage + "Taken.")

        if "taken" not in item.traits:
            item.traits.append("taken")
        if item.take_func:
            item.take_func(imp, context)
        item.container = context.player
TakeHandler = VerbFunction("take_handler", take_handler, True, False)


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
        item.conatiner = curr_loc
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
            elif not obstacle.closable:
                my_print("des", "That's not something you can close.")
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

    container = context.ido[0]

    for object in context.do:
        # Define pre-message to potentially append to print statements.
        if len(context.do) == 1:
            premessage = ""
        else:
            premessage = object.type + ": "

        # Make sure player didn't try to put an item inside of itself or item is not holding container
        if object.name == container.name:
            my_print("des", premessage + "'There are two types of people in this world: Those who don't believe in infinite recursion and those that believe 'There are two types of people in this world...''")
            continue

        # Make sure object is not holding container
        if container.container.name == object.name:
            my_print("des", premessage + "The " + object.type + " is already holding the " + container.type + ".")
            continue

        # Make sure object is not already in container
        if object.name in container.inv.item_map:
            my_print("des", premessage + "The " + object.type + " is already inside of the " + container.type + ".")
            continue

        # Make sure the IDO is actually a container
        if container.classname == 'vault':
            imp.set_verb("insert")
            container.funcs[imp.verb](imp, context)
            continue
        if container.classname != 'container':
            my_print("des", premessage + "That can't contain things.")
            continue

        # Check to make sure container is open and has room
        if container.closed:
            my_print("des", premessage + "The " + container.name + " is not open.")
            continue

        # Divert to liquid function if needed
        if "liquid" in object.traits:
            try:
                imp.set_verb("fill")
                container.funcs[imp.verb](imp, context)
            except:
                my_print("des", premessage + "It's best not to put that in there.")
            continue

        if not container.inv.add_item(object):
            if object.weight > container.inv.capacity:
                my_print("des", premessage + "You can't possibly fit that in there!")
            else:
                my_print("des", premessage + "The " + container.name + " is already full.")
            continue

        # Remove from player's inventory if necessary
        if object.name in context.player.inv.item_map:
            if not context.player.inv.remove_item(object):
                my_print("err", "put_handler: failed to remove", object.name, "from player inventory.")

        # Otherwise, remove from environment
        elif object.name in context.map[context.current_loc].inv.item_map:
            my_print("des", "(first taking the " + object.name + ")")
            if not context.map[context.current_loc].inv.remove_item(object):
                my_print("err", "put_handler: failed to remove", object.name, "from surrounding.")

        object.container = container
        my_print("des", premessage + "You put the " + object.name + " in the " + container.name + ".")
    return
PutHandler = VerbFunction("put_handler", put_handler, True, True, ido_missing="Where")


def inv_handler(imp, context):
    if context.player.inv.weight == 0:
        my_print("des", "You are empty handed.")
    else:
        # Assemble equipment and true inventory
        equipment = []
        true_inv = []
        for item in context.player.inv.item_map.values():
            if "equipped" in item.traits:
                equipment.append(item)
            else:
                true_inv.append(item)

        my_print("des", "You are carrying:")
        for item in true_inv:
            my_print("des", item.des)
            if item.classname == "container" and item.inv.item_map:
                my_print("des", "The " + item.name + " contains:")
                for sub_item in item.inv.item_map.values():
                    my_print("des", sub_item.des)

        if equipment:
            my_print("des", "")
            my_print("des", "You are wearing:")
            for item in equipment:
                my_print("des", item.des)
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


def read_handler(imp, context):
    for item in context.do:
        if 'readable' not in item.traits:
            if len(context.do) == 1:
                my_print("des", "That's not something you can read.")
            else:
                my_print("des", item.name + ": " + "That's not something you can read.")

        else:
            item.item_func(imp, context)
ReadHandler = VerbFunction("read_handler", read_handler, True, False)


def examine_handler(imp, context):
    if len(context.do) > 1:
        my_print("des", "You can only examine one object at a time.")
    else:
        my_print("des", context.do[0].des)
ExamineHandler = VerbFunction("examine_handler", examine_handler, True, False)


def liquid_handler(imp, context):
    if context.do and context.do[0].classname == "container":
        bucket = context.do[0]
    elif context.ido and context.ido[0].classname == "container":
        bucket = context.ido[0]

    bucket.funcs[imp.verb](imp, context)
LiquidHandler = VerbFunction("liquid_handler", liquid_handler, True, True)


verb_functions = {"go": MoveHandler, "move": MoveHandler, "run": MoveHandler, "walk": MoveHandler, "tp": TpHandler,
                  "take": TakeHandler, "get": TakeHandler, "grab": TakeHandler, "obtain": TakeHandler,
                  "drop": DropHandler,
                  "open": OpenHandler,
                  "close": CloseHandler, "shut": CloseHandler, "slam": CloseHandler,
                  "inventory": InvHandler,
                  "put": PutHandler, "place": PutHandler, "insert": PutHandler,
                  "look": LookHandler, "observe": LookHandler,
                  "break": BreakHandler, "destroy": BreakHandler, "chop": BreakHandler,
                  "equip": EquipHandler,
                  "dequip": DequipHandler, "remove": DequipHandler,
                  "read": ReadHandler,
                  "examine": ExamineHandler,
                  "fill": LiquidHandler, "pour": LiquidHandler, "empty": LiquidHandler}


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
        my_print("log", "No DO found when one was needed")
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
