from classes.player import Player
from classes.locations import Location, Obstacle, Vault
from classes.inventory import Item, Inventory, Container


BLOCKED = None


class Context:
    def __init__(self, player, map):
        self.player = player
        self.current_loc = "cornfield south"
        self.map = map
        self.moves = 0
        self.score = 0
        self.do = []
        self.ido = []
        self.tmp_items = []

    def refresh(self):
        self.do = []
        self.ido = []
        self.tmp_items = []

    def print(self):
        print("\nLOCATION       : " + self.current_loc)
        print("MOVES          : " + str(self.moves))
        print("SCORE          : " + str(self.score))
        print("---- DOs ----")
        for do in self.do:
            print(do.name)
        print("---- IOs ----")
        for ido in self.ido:
            print(ido.name)
        print("---- TMP ----")
        for item in self.tmp_items:
            print(item)
        print("\n")

    def find_object(self, imp, dont_search, mode):
        curr_loc = self.map[self.current_loc]

        if mode == 'do':
            object_location = self.do
            imp_ob = imp.noun
            imp_adjs = imp.nounq
        elif mode == 'ido':
            object_location = self.ido
            imp_ob = imp.second
            imp_adjs = imp.secondq
        else:
            print("INVALID MODE ENTERED FIND_OBJECT:", mode)
            return
        print("Step - find_object:", imp_ob[0][0])

        # If all keyword specified, searching all relevant items
        if imp_ob[0][0] == 'all':
            if 'obstacles' not in dont_search:
                for key in curr_loc.obstacles:
                    object_location.append(curr_loc.obstacles[key])
            if 'surroundings' not in dont_search:
                for key in curr_loc.inv.item_map:
                    object_location.append(curr_loc.inv.item_map[key])
            if 'inventory' not in dont_search:
                for key in self.player.inv.item_map:
                    object_location.append(self.player.inv.item_map[key])
            return

        # First search location for obstacles
        if 'obstacle' not in dont_search:
            obstacle = curr_loc.find_obstacle(imp, self, imp_ob[0][0], imp_adjs[0])
            if obstacle:
                print("Found obstacle", obstacle.name)
                object_location.append(obstacle)
                self.tmp_items = []
                return

        # Next search location for regular items
        if 'surroundings' not in dont_search:
            surroundings_item = curr_loc.inv.find(imp, self, imp_ob[0][0], imp_adjs[0])
            if surroundings_item:
                print("Found surroudings", surroundings_item.name)
                object_location.append(surroundings_item)
                self.tmp_items = []
                return

        # Finally, search player inventory
        if 'inventory' not in dont_search:
            player_item = self.player.inv.find(imp, self, imp_ob[0][0], imp_adjs[0])
            if player_item:
                print("Found inventory", player_item.name)
                object_location.append(player_item)
                self.tmp_items = []
                return

        # Didn't find anything
        print("You can't see any such thing.")


def farmhousew_door_func(imp, context):
    farmhousew = context.map["farmhouse west"]
    kitchen = context.map["kitchen"]
    door = farmhousew.obstacles["farmhouse west door"]
    if door.status:
        print("You swing the door open.")
        farmhousew.e = "kitchen"
        kitchen.w = "farmhouse west"
        door.status = False
    else:
        print("You slam the door shut. Jeez, be gentle...")
        farmhousew.e = BLOCKED
        kitchen.w = BLOCKED
        door.status = True


def barnhouse_door_func(imp, context):
    print("Success!")


def fireplace_vault_func(imp, context):
    fire_room = context.map["fire room"]
    fireplace = fire_room.obstacles["adorned fireplace"]
    if imp.verb == 'insert':
        if context.do[0].name not in fireplace.req_locks:
            print("It doesn't seem to fit.")
            return
        fireplace.inv.add_item(context.do[0])
        context.player.inv.remove_item(context.do[0])
        print("The " + context.do[0].name + " clicks into place nicely.")

        if 'copper key' in fireplace.inv.item_map and \
           'jade key' in fireplace.inv.item_map and \
           'crystal key' in fireplace.inv.item_map:
            fireplace.locked = False
            print("You hear a loud mechanism clunk open.")

    elif imp.verb == 'open' or imp.verb == 'close':
        if fireplace.locked:
            print("You try, but the sparkling stones hold fast.")
        else:
            if fireplace.closed:
                print("The fireplace swings outward revealing a hidden vault.")
                fireplace.closed = False
            else:
                print("The fireplace swings shut with a mighty thud.")
                fireplace.closed = True


def gen_context():
    # Items and inventories
    axe = Item("wood ax", "ax", "A gleaming wood ax", 20, syns=["ax", "axe"])
    weight = Item("heavy weight", "weight", "A very heavy weight", 100)
    barn_inv = Inventory(100000, [axe, weight])
    copper_key = Item("copper key", "copper key", "A tarnished copper key", 1, syns=["key"], adjs=["copper", "red"])
    jade_key = Item("jade key", "jade key", "A vibrant jade key", 1, syns=["key"], adjs=["jade", "green"])
    crystal_key = Item("crystal key", "crystal key", "A beautiful crystal key", 1, syns=["key"], adjs=["crystal"])
    keyring = Inventory(100000, [copper_key, jade_key, crystal_key])
    bottle = Item("bottle", "bottle", "A clear glass soda bottle", 1, syns=["bottle"], adjs=["glass", "clear"])
    lunchbox = Item("lunchbox", "lunchbox", "A vintage metal lunchbox", 2, syns=["lunchbox", "box"], adjs=["vintage", "metal"])
    kitchen_inv = Inventory(100000, [bottle, lunchbox])

    # Obstacles
    farmhousew_door = Obstacle("farmhouse west door", "door", "A sturdy looking door, painted black", 101,
                               verbs=["open", "push", "enter"], syns=["door"], adjs=["black"],
                               funcs={"open": farmhousew_door_func, "close": farmhousew_door_func})
    barnhouse_door = Obstacle("barnhouse door", "door", "A deteriorating wooden door", 101,
                              breakable=True, verbs=["break", "chop", "destroy"], syns=["door"], adjs=["wooden"],
                              funcs={"break": barnhouse_door_func})

    # Vaults
    fireplace_vault = Vault("adorned fireplace", "fireplace", "A beautifully adorned fireplace crafted from dozens of polished gems and precious stones. Three keyholes lie in a trifecta; one in rusted red-green metal, one in vibrant and polished green, and the last in shining quartz.",
                            101, short_des="An adorned fireplace", inv=Inventory(3, []), verbs=["insert", "unlock"], syns=["fireplace", "vault", "keyhole", "lock"],
                            funcs={"insert": fireplace_vault_func, "open": fireplace_vault_func, "close": fireplace_vault_func},
                            can_remove=False, req_locks=["copper key", "jade key", "crystal key"])

    # Locations
    cornfield1 = Location("cornfield south", "Cornfield South", keyring,
                     "This is a musty cornfield, full of dusty dead stalks. It continues to the north. A farm lies to the south.",
                     n="cornfield north", s="silos")
    cornfield2 = Location("cornfield north", "Cornfield North", Inventory(100000),
                          "This is a musty cornfield, full of dusty dead stalks. It continues to the south. A small river lies to the north.",
                          n="river cross", s="cornfield south")
    river = Location("river cross", "River Crossing", Inventory(100000),
                     "This is a river, swift and strong. The path runs through the river northwest to south. It looks shallow enough to wade through, but the current would sweep you away.",
                     s="river cross", nw="homestead")
    silos = Location("silos", "Twin Silos", Inventory(100000),
                     "Two massive silos stand defiant against the surrounding terrain. A large barn sits to the west. A small farmhouse to the south is nearly obscured by their massive stature. A deteriorating ladder is bolted to the side of one, if only there were a better way up...",
                     n="cornfield south", s="farmhouse west", w="barn", se="front yard")
    barn = Location("barn", "Old Barn", barn_inv,
                    "This is a dusty old barn full of disintegrating hay and rusty tools. A cornfield lies to the east. There is a workshed to the immediate south. You can hear a chorus of frogs to the northwest.",
                    s=BLOCKED, e="silos", nw="frog pond",
                    obstacles={barnhouse_door.name: barnhouse_door}, ob_messages={"south": "The door is closed."})
    workshop = Location("workshop", "Workshop", Inventory(100000),
                        "This is a moderately sized workshop. Dozens of alien tools are hung neatly from the walls, although you recognize none of them. There are doors on the north and east walls of the workshop.",
                        n=BLOCKED, e="farmhouse west",
                        obstacles={barnhouse_door.name: barnhouse_door}, ob_messages={"north": "The door is closed."})
    farmhousew = Location("farmhouse west", "West of Farmhouse", Inventory(100000),
                         "You are facing the west side of a beautiful farmhouse. You can see a door facing you. The large silos lies to the north. A gravel path runs to the south east. A large farm building stands steadfast to the west.",
                         n="silos", s="south farmhouse", e=BLOCKED, w="workshop", sw="firepits",
                          obstacles={farmhousew_door.name: farmhousew_door}, ob_messages={"east": "The door is closed."})
    farmhouses = Location("south farmhouse", "South of Farmhouse", Inventory(100000),
                          "You are facing the south side of a beautiful farmhouse. A small toolshed is next to a large gas tanker, but they both appear to be empty.",
                          s="hay field", w="farmhouse west", e="front yard")
    kitchen = Location("kitchen", "Kitchen", kitchen_inv,
                       "You are in a dusty but tidy kitchen. Several large cupboards line the walls. A half-played boardgame lies abandoned on a large wooden table. A doorway into an ornately furnished living room. On the southern wall is a door to outside. ",
                       e="fire room", w=BLOCKED,
                       obstacles={farmhousew_door.name: farmhousew_door}, ob_messages={"west": "The door is closed."})
    fireroom = Location("fire room", "Living Room", Inventory(100000),
                        "You are in a beautifully furnished living room. An enormous moose head is mounted against the south wall. A full bookshelf lies on either side of the moose. However, the room is visually dominated by a massive stone fireplace on the north wall. Instead of bedrocks, each stone in the fireplace is ornately inscribed and appears of precious origin. Three keyholes are embedded in three different stones; one reddish, one bright green, and one of clear quartz.",
                        e="front yard", w="kitchen",
                        obstacles={fireplace_vault.name: fireplace_vault})
    frontyard = Location("front yard", "Front Yard", Inventory(100000),
                         "This is a long yard stretching west to east. Despite everything else in and around the house being old and dusty, the lawn is neatly manicured. You can hear a small brook burbling past the end of the lawn.",
                         e="creek3", w="fire room", nw="silos")
    vineyarde = Location("vineyard east", "Vineyard East", Inventory(100000),
                        "This is an unruly but splendid vineyard. Large purple grapes dot several trellises along ordered rows. A sign states 'The Merlin of Merlot: Verita's Finest Wine Grapes'. Behind you to the east is a hay field. The vineyard continues to the west.",
                        e="hay field", w="vineyard west")
    vineyardw = Location("vineyard west", "Vineyard West", Inventory(100000),
                         "This is an unruly but splendid vineyard. Large purple grapes dot several trellises along ordered rows. The vineyard continues to the east. A small clearing is to the north.",
                         n="firepits", e="vineyard east")
    firepits = Location("firepits", "Fire Pits", Inventory(100000),
                         "There are 3 deep fire pits here, each marked by a ring of rough stones. Piles of ashes and charred wood lie in each pit. You can see something gleaming just under the ashes in one pit.",
                         s="vineyard west", ne="farmhouse west")
    creek1 = Location("creek1", "Bubbling Creek", Inventory(100000),
                      "The creek is pouring out of a large wellspring to the north. It looks just large enough for you to enter...",
                      n="cave", s="creek2")
    creek2 = Location("creek2", "Bubbling Creek", Inventory(100000),
                      "This is a gentle, bubbling creek running north to south.",
                      n="creek1", s="creek3")
    creek3 = Location("creek3", "Bubbling Creek", Inventory(100000),
                      "This is a gentle, bubbling creek running north to south.",
                      n="creek2", s="creek4", w="front yard")
    creek4 = Location("creek4", "Bubbling Creek", Inventory(100000),
                      "This is a gentle, bubbling creek running north to south. You can see a larger body of water to the south.",
                      n="creek3", s="lagoon", sw="dock")
    lagoon = Location("lagoon", "Scummy Lagoon", Inventory(100000),
                      "This is a stagnant lagoon, covered in algae and green muck. A deteriorating dock is rotting to the east. A rowboat sits adrift in the middle of the lagoon, far out of your reach.",
                      n="creek4", w="dock")
    dock = Location("dock", "Rotted Dock", Inventory(100000),
                    "This is a very old and nearly rotten wooden dock. A rowboat sits calmly in the center of the lake, perhaps 15 feet from the edge of the dock.",
                    e="lagoon", n="creek4")
    cave = Location("cave", "Cave Mouth", Inventory(100000),
                    "This is the entrance to a small cave. The creek appears to flows from further up the cave to the northeast, but the passage is entirely submerged. You do not see any other passages.",
                    s="creek1", ne="flooded passage")
    flooded_passage = Location("flooded passage", "Cave Passage", Inventory(100000),
                               "This is a narrow cave passage going northeast to southwest. The passage is totally submerged, but it's wide enough for you to swim through.",
                               sw="cave", ne="grotto")
    grotto = Location("grotto", "Hidden Grotto", Inventory(100000),
                      "You appear to be in a hidden underground grotto. A faint light comes from a variety of phosphorescent algae and fungi growing about the space. A deep pool lies in the center of the grotto. Several large rocks bear primitive inscriptions on them, but you are unable to decipher their meaning.",
                      sw="flooded passage")
    hayfield = Location("hay field", "Field of Hay", Inventory(100000),
                        "This is an expansive field of hay. It has clearly been some time since the last harvest. A trail runs off to the north and south. You can see a gravel path at the edge of the field to the west.",
                        n="south farmhouse", s="graveyard", w="vineyard east")
    graveyard = Location("graveyard", "Graveyard", Inventory(100000),
                         "This is a small graveyard. Roughly a dozen or two tombstombs hold a silent vigil over the hallowed ground. Most of their inscriptions are too old to read, but you can make out the writing on one of them. Dirt tire tracks lead off to the west. A trail runs to the north.",
                         n="hay field", w="tire tracks1")
    tires1 = Location("tire tracks1", "Tire Tracks", Inventory(100000),
                      "This is a set of tire tracks, likely from a moderately sized ATV. They run to the east and the west. You are now surrounded in a thick forest.",
                      e="graveyard", w="tire tracks2")
    tires2 = Location("tire tracks2", "Tire Tracks", Inventory(100000),
                      "This is a set of tire tracks, likely from a moderately sized ATV. They run to the east and the west. You can see some kind of stone building poking its head above the trees to the west.",
                      e="tire tracks1", w="lone tower")
    tower = Location("lone tower", "Lonesome Tower", Inventory(100000),
                     "This is a large tower with a turret roof. The tower has a single door and several windows. The forest is very dense here. Dirt tracks run off to the east.",
                     e="tire tracks2")
    homestead = Location("homestead", "Homestead", Inventory(100000),
                         "This is a derelict homestead. At one point it time, it may have been a comfortable frontier home. Now it is barely recognizible. The path continues to the southwest and to the southeast.",
                         se="river cross", sw="water well")
    well = Location("water well", "Water Well", Inventory(100000),
                    "This is a natural wellspring. Several wild cows drinking at the spring block your way to the water. The path continues to the northeast and northwest.",
                    ne="river cross", nw="turkey blind")
    turkey = Location("turkey blind", "Turkey Blind", Inventory(100000),
                      "This is an old turkey blind underneath a large oak. Stacks of logs neatly enclose a small camoflauge tent. The path continues to the southwest and southeast.",
                      se="water well", sw="forest path1")
    forestpath1 = Location("forest path1", "Forest Path", Inventory(100000),
                          "This is a well-used path through the forest. A variety of animal tracks are imprinted in the dirt. The path continues to the south and northeast.",
                          s="strange circle", ne="turkey blind")
    circle = Location("strange circle", "Strange Circle", Inventory(100000),
                      "You are in a forest clearing that can only be described as odd. A circle of worn monolithic stones stand silent vigil in the center of the clearing. The grass is slightly browned in a way that creates intricate patterns around the stones. Paths branch off to the north, south, and east.",
                      n="forest path1", s="forest path2", e="large oak")
    oak = Location("large oak", "Large Oak", Inventory(100000),
                   "This is an massive white oak. Its branches are easily several feet thick and its root snake out dozens of meters in all directions. You can see a small clearing to the west. A path cuts through the forest to the south. You can hear a chorus of frogs to the southeast.",
                   w="strange circle", s="forest path3", se="frog pond")
    forestpath2 = Location("forest path2", "Forest Path", Inventory(100000),
                           "This is a well-used path through the forest. The trees around you are particularly thick here. The path curves from the north to the east.",
                           n="strange circle", e="forest path3")
    forestpath3 = Location("forest path3", "Forest Path", Inventory(100000),
                           "This is a well-used path through the forest. The trees around you are beginning to thin out a bit. The path curves from the west to the north, but you can probably make your own way to the east.",
                           n="large oak", e="frog pond", w="forest path2")
    frogpond = Location("frog pond", "Frog Pond", Inventory(100000),
                        "This is a large, scummy pond. The croaking of the frogs is nearly deafening here. There must be hundreds hiding in the undergrowth. Thick cattails and other marsh plants grow around the pond's edge. A path continues to the west and to the southeast",
                        w="forest path3", se="barn")



    map = {"cornfield south": cornfield1, "barn": barn, "farmhouse west": farmhousew, "silos": silos, "kitchen": kitchen,
           "fire room": fireroom, "front yard": frontyard, "creek1": creek1, "creek2": creek2, "creek3": creek3,
           "creek4": creek4, "lagoon": lagoon, "dock": dock, "cave": cave, "flooded passage": flooded_passage,
           "grotto": grotto, "south farmhouse": farmhouses, "hay field": hayfield, "graveyard": graveyard, "tire tracks1": tires1,
           "tire tracks2": tires2, "lone tower": tower, "vineyard east": vineyarde, "vineyard west": vineyardw,
           "firepits": firepits, "workshop": workshop, "cornfield north": cornfield2, "river cross": river,
           "homestead": homestead, "water well": well, "turkey blind": turkey, "forest path1":  forestpath1,
           "strange circle": circle, "large oak": oak, "forest path2": forestpath2, "forest path3": forestpath3,
           "frog pond": frogpond}

    player = Player()

    context = Context(player, map)

    return context