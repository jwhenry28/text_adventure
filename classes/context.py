from classes.player import Player
from classes.locations import Location
from classes.inventory import Item, Inventory


class Context:
    def __init__(self, player, map):
        self.player = player
        self.map = map
        self.moves = 0
        self.score = 0


def gen_context():
    axe = Item("ax", "A gleaming wood ax", 20)
    weight = Item("weight", "A very heavy weight", 100)
    barn_inv = Inventory(100000, [axe, weight])

    cornfield1 = Location("cornfield south", "Cornfield South", Inventory(100000),
                     "This is a musty cornfield, full of dusty dead stalks. A farm lies to the south.",
                     s="silos")
    silos = Location("silos", "Twin Silos", Inventory(100000),
                     "Two massive silos stand defiant against the surrounding terrain. A small farmhouse to the south is nearly obscured by their massive stature. A deteriorating ladder is bolted to the side of one, if only there were a better way up...",
                     n="cornfield south", s="west farmhouse", w="barn", se="front yard")
    barn = Location("barn", "Old Barn", barn_inv,
                    "This is a dusty old barn full of disintegrating hay and rusty tools. A cornfield lies to the east. There is a workshed to the immediate south.",
                    s="workshop", e="silos")
    workshop = Location("workshop", "Workshop", Inventory(100000),
                        "This is a moderately sized workshop. Dozens of alien tools are hung neatly from the walls, although you recognize none of them. There are doors on the north and east walls of the workshop.",
                        n="barn", e="west farmhouse")
    wfarmhouse = Location("west farmhouse", "West of Farmhouse", Inventory(100000),
                         "You are facing the west side of a beautiful farmhouse. You can see a door facing you. The large silos lies to the north. A gravel path runs to the south east. A large farm building stands steadfast to the west.",
                         n="silos", s="south farmhouse", e="kitchen", w="workshop", sw="firepits")
    sfarmhouse = Location("south farmhouse", "South of Farmhouse", Inventory(100000),
                          "You are facing the south side of a beautiful farmhouse. A small toolshed is next to a large gas tanker, but they both appear to be empty.",
                          s="hay field", w="west farmhouse", e="front yard")
    kitchen = Location("kitchen", "Kitchen", Inventory(100000),
                       "You are in a dusty but tidy kitchen. Several large cupboards line the walls. A half-played boardgame lies abandoned on a large wooden table. A doorway into an ornately furnished living room. On the southern wall is a door to outside. ",
                       e="fire room", w="west farmhouse")
    fireroom = Location("fire room", "Living Room", Inventory(100000),
                        "You are in a beautifully furnished living room. An enormous moose head is mounted against the south wall. A full bookshelf lies on either side of the moose. However, the room is visually dominated by a massive stone fireplace on the north wall. Instead of bedrocks, each stone in the fireplace is ornately inscribed and appears of precious origins.",
                        e="front yard", w="kitchen")
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
                         s="vineyard west", ne="west farmhouse")
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


    map = {"cornfield south": cornfield1, "barn": barn, "west farmhouse": wfarmhouse, "silos": silos, "kitchen": kitchen,
           "fire room": fireroom, "front yard": frontyard, "creek1": creek1, "creek2": creek2, "creek3": creek3,
           "creek4": creek4, "lagoon": lagoon, "dock": dock, "cave": cave, "flooded passage": flooded_passage,
           "grotto": grotto, "south farmhouse": sfarmhouse, "hay field": hayfield, "graveyard": graveyard, "tire tracks1": tires1,
           "tire tracks2": tires2, "lone tower": tower, "vineyard east": vineyarde, "vineyard west": vineyardw,
           "firepits": firepits, "workshop": workshop}

    player = Player()

    context = Context(player, map)

    return context