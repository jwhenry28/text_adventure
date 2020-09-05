from nltk.tokenize import word_tokenize
from nltk import pos_tag, RegexpParser
from nltk.corpus import stopwords
import re


class Imperative:
    def __init__(self):
        self.actor = "I"
        self.verb = None
        self.nounq = []
        self.noun = []
        self.secondq = []
        self.second = []

    def is_bogus(self):
        if not self.verb:
            return True
        return False

    def set_verb(self, verb):
        self.verb = verb

    def set_nounq(self, nounq):
        self.nounq.append(nounq)

    def set_noun(self, noun):
        self.noun.append(noun)

    def set_secq(self, secondq):
        self.secondq.append(secondq)

    def set_second(self, second):
        self.second.append(second)

    def remove_noun(self):
        del(self.noun[0])
        del(self.nounq[0])

    def remove_second(self):
        del(self.second[0])
        del(self.secondq[0])

    def print(self):
        print("ACTOR   : " + self.actor)
        if self.verb:
            print("VERB    : " + self.verb)
        else:
            print("VERB    : ---")
        print("NOUN    :", self.noun)
        print("NOUNQ   :", self.nounq)
        print("SECOND  :", self.second)
        print("SECONDQ :", self.secondq)
        print("\n")


# Utility functions
def get_prep(string):
    if string[0] in ['a', 'e', 'i', 'o', 'u']:
        return 'an'
    return 'a'


nounless_verbs = ["look"]
directions = ["n", "s", "e", "w", "ne", "nw", "se", "sw", "u", "d",
              "north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest", "up", "down"]
verbs = ["go", "take", "drop", "kill", "open", "close", "look", "observe", "insert", "put", "place", "break", "chop",
         "destroy"]
nouns = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest", "n", "s", "e", "w", "ne",
         "nw", "se", "sw", "u", "d", "up", "down", "ax", "axe", "key", "keys", "troll", "door", "crowbar", "all",
         "sword", "bottle", "lunchbox", "lunch", "box", "fireplace", "vault", "keyhole", "lock", "tome", "book",
         "manuscript"]
adjectives = ["jade", "small", "copper", "rusty", "crystal", "red", "green", "wooden", "black"]
conjunctions = ["and"]
prepositions = ["with", "on", "but", "in", "into"]


def regex_imperative():
    movement_rule = \
        "^(s(outh)?$|n(orth)?$|e(ast)?$|w(est)?$|south ?west|sw|south ?east|se|north ?west|nw|north ?east|ne|up|down)"
    inventory_rule = "^inventory$|^inv$|^i$"
    debug_rule = "^tp .*$"

    command = input("> ")
    movement_check = re.search(movement_rule, command)
    inventory_check = re.search(inventory_rule, command)
    debug_check = re.search(debug_rule, command)

    imp = Imperative()
    ido_flag = False
    unknown = None

    # Inventory - no noun needed
    if inventory_check:
        imp.set_verb("inventory")
    # Fast move
    elif movement_check:
        imp.set_verb("go")
        imp.set_noun([command])
        imp.set_nounq([])
    # Debug rules - dependent on the command
    elif debug_check:
        words = word_tokenize(command)
        if words[0] == 'tp':
            imp.set_verb('tp')
            imp.set_noun([command[3:]])
    # Normal parsing
    else:
        words = word_tokenize(command)
        first = words.pop(0)
        imp.set_verb(first)
        # tmp used to store each individual item's adjectives
        tmp = []
        for word in words:
            # Nouns
            if word in nouns:
                if ido_flag:
                    imp.set_second([word])
                    imp.set_secq(tmp)
                else:
                    imp.set_noun([word])
                    imp.set_nounq(tmp)
            # Adjectives
            elif word in adjectives:
                if ido_flag:
                    tmp.append(word)
                else:
                    tmp.append(word)
            # Conjunctions & Prepositions
            elif word in prepositions:
                ido_flag = True
                tmp = []
            elif word in conjunctions:
                tmp = []
            else:
                unknown = word

    # Put bogus value in if unknown word encountered and no known
    if unknown and not imp.noun:
        imp.set_noun([unknown])
        imp.set_nounq([])

    imp.print()

    return imp


# Used to parse a partial input, when ambiguous items need clarification.
def mini_parse(imp, clarification, mode):
    words = word_tokenize(clarification)

    if mode == 'do':
        ido_flag = False
    elif mode == 'ido':
        ido_flag = True
    else:
        print("INVALID MODE GIVEN:", mode)
        return

    # tmp used to store each individual item's adjectives
    tmp = []
    for word in words:
        # Nouns
        if word in nouns:
            if ido_flag:
                imp.set_second([word])
                imp.set_secq(tmp)
            else:
                imp.set_noun([word])
                imp.set_nounq(tmp)
        # Adjectives
        elif word in adjectives:
            if ido_flag:
                tmp.append(word)
            else:
                tmp.append(word)
        # Conjunctions & Prepositions
        elif word in prepositions:
            ido_flag = True
            tmp = []
        elif word in conjunctions:
            tmp = []
        else:
            unknown = word

    return imp
