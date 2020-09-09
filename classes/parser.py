from nltk.tokenize import word_tokenize
from website_utils.utils import my_print, my_input
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

    def overwrite_nounq(self, nounq):
        self.nounq[0] = nounq

    def set_noun(self, noun):
        self.noun.append(noun)

    def set_secq(self, secondq):
        self.secondq.append(secondq)

    def overwrite_secq(self, secq):
        self.secq[0] = secq

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
         "destroy", "equip"]
nouns = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest", "n", "s", "e", "w", "ne",
         "nw", "se", "sw", "u", "d", "up", "down", "ax", "axe", "key", "keys", "troll", "door", "crowbar", "all",
         "sword", "bottle", "lunchbox", "lunch", "box", "fireplace", "vault", "keyhole", "lock", "tome", "book",
         "manuscript"]
adjectives = ["jade", "small", "copper", "rusty", "crystal", "red", "green", "wooden", "black", "white", "closet", "odd"]
conjunctions = ["and"]
prepositions = ["with", "on", "but", "in", "into"]


def regex_imperative(command):
    movement_rule = \
        "^(s(outh)?$|n(orth)?$|e(ast)?$|w(est)?$|south ?west|sw|south ?east|se|north ?west|nw|north ?east|ne|up|down)|u(p)?|d(own)?"
    inventory_rule = "^inventory$|^inv$|^i$"
    debug_rule = "^tp .*$"
    pickup_rule = "^pick up .*$"
    putton_rule = "^put on .*$"

    movement_check = re.search(movement_rule, command)
    inventory_check = re.search(inventory_rule, command)
    debug_check = re.search(debug_rule, command)
    pickup_check = re.search(pickup_rule, command)
    putton_check = re.search(putton_rule, command)

    imp = Imperative()
    ido_flag = False
    unknown = None
    normal_parse = True
    words = word_tokenize(command)

    # Return nothing if nothing was empty
    if not words:
        return None

    # Inventory - no noun needed
    if inventory_check:
        imp.set_verb("inventory")
        normal_parse = False
    # Fast move
    elif movement_check:
        imp.set_verb("go")
        imp.set_noun([command])
        imp.set_nounq([])
        normal_parse = False
    # Debug rules - dependent on the command
    elif debug_check:
        if words[0] == 'tp':
            imp.set_verb('tp')
            imp.set_noun([command[3:]])
        normal_parse = False
    # Pick up rules - since pick up is not a one-word verb
    elif pickup_check:
        imp.set_verb("take")
        words.pop(0)
        words.pop(0)
    elif putton_check:
        imp.set_verb("equip")
        words.pop(0)
        words.pop(0)
    # Regular format
    else:
        first = words.pop(0)
        imp.set_verb(first)

    # Normal parsing
    if normal_parse:
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
def mini_parse(imp, clarification, ob_mode, adj_mode=False):
    words = word_tokenize(clarification)

    adj_flag = adj_mode
    if ob_mode == 'do':
        ido_flag = False
    elif ob_mode == 'ido':
        ido_flag = True
    else:
        my_print("err", "INVALID MODE GIVEN:", ob_mode)
        return

    # tmp used to store each individual item's adjectives
    tmp = []
    if not adj_flag:
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
    else:
        for word in words:
            # Adjectives
            if word in adjectives:
                tmp.append(word)
        if ob_mode == 'do':
            imp.overwrite_nounq(tmp)
        else:
            imp.overwrite_secq(tmp)

    return imp
