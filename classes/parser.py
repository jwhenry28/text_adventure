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


nounless_verbs = ["look"]
directions = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest",
              "n", "s", "e", "w", "ne", "nw", "se", "sw", "up", "down"]
verbs = ["go", "take", "drop", "kill", "open", "close", "look"]
nouns = ["north", "south", "east", "west", "northeast", "northwest", "southeast", "southwest", "n", "s", "e", "w", "ne",
         "nw", "se", "sw", "up", "down", "ax", "axe", "key", "keys", "troll", "door", "crowbar", "all", "sword",
         "bottle", "lunchbox", "lunch", "box"]
adjectives = ["jade", "small", "copper", "rusty", "crystal"]
conjunctions = ["and"]
prepositions = ["with", "on", "but"]


def get_imperative():
    var = True
    while var:
        # Gather input
        text = input("> ").lower()

        if text == "":
            continue

        # Tokenize & Tag into POS
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        words.insert(0, "I")
        if len(words) > 2 and words[2] != "the":
            words.insert(2, "the")

        # Add "the" after proposition if one exists (ik this is shitty, but parsing is tough)
        thrown = False
        direction_parsing = False
        for i in range(0, len(words)):
            if words[i] == 'with' or words[i] == 'to':
                try:
                    if words[i + 1] != 'the':
                        words.insert(i + 1, 'the')

                except Exception as e:
                    print(words[i], "what?")
                    thrown = True
            elif words[i] in directions:
                # This should only occur once; otherwise this is a nonsensical sentence
                if not direction_parsing:
                    direction_parsing = True
                else:
                    break

                if "go" not in words:
                    words.insert(i, "go")

                try:
                    if words[i+1] != "the":
                        words.insert(i+1, "the")
                except:
                    break

        # Retry if no indirect object was given
        if thrown:
            thrown = False
            continue

        # Tag Parts of speech
        tagged = pos_tag(words)

        # Create Rule
        master_rule = r"""master_chunk: {<PRP><VB.?><.*>*<NN><.*>*<NN>?}"""
        master_parser = RegexpParser(master_rule)
        master_chunk = master_parser.parse(tagged)

        # Make sure the rule is followed
        formatted = []
        if master_chunk.height() == 3:
            popped = master_chunk.pop()
            formatted = [w for w in popped if not w[1] in stop_words]

        # Start over if there is no direct object
        # THIS SECTION NEEDS OVERHAUL
        else:
            if master_chunk[1][1][0:2] == 'VB':
                if len(master_chunk) == 2:
                    print(master_chunk[1][0] + " what?")
                    continue
                # Unless verb does not require a direct object
                if master_chunk[1][0] in nounless_verbs:
                    formatted = [w for w in master_chunk if not w[0] in stop_words]
                # Or you are indicating to go up/down
                elif master_chunk[3][0] == 'up' or master_chunk[3][0] == 'down':
                    formatted = [w for w in master_chunk]
                    formatted[3] = (formatted[3][0], 'NN')
                else:
                    print(master_chunk[1][0] + " what?")
                    continue

            else:
                print("That's not a verb I recognise.")
                continue

        # Parse command into Imperative object
        imp = Imperative()
        second = False
        for item in formatted:
            # Filter out unnecessary words
            if item[1] == 'PRP' or item[1] == 'DT':
                continue

            # Everything after preposition SHOULD be indirect object related
            if item[1] == 'IN':
                second = True

            if item[1][0:2] == 'VB':
                imp.set_verb(item[0])
            elif item[1][0:2] == 'JJ':
                if second:
                    imp.set_secq(item[0])
                else:
                    imp.set_nounq(item[0])
            elif item[1][0:2] == 'NN':
                if second:
                    imp.set_second(item[0])
                else:
                    imp.set_noun(item[0])

        var = False

    return imp


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

    # Program didn't recognize the sentence; just guess as to what is what
    if imp.is_bogus():
        print("BOGUS")
        imp.print()
        imp.set_noun()
        imp.set_nounq([])

    # imp.print()

    return imp


# Used to parse a partial input, when ambiguous items need clarification
def mini_parse(imp, clarification, mode):
    words = word_tokenize(clarification)

    if mode == 'do':
        imp.set_nounq(words)
    elif mode == 'ido':
        imp.set_secq(words)
    else:
        print("INVALID MODE GIVEN:", mode)

    return imp



    return imp
