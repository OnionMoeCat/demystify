
# Because Magic is essentially a subset of English language, we need to
# include multiple parts of speech for every word. For verbs, we need
# present and past tenses, sometimes progressive tense, and occasionally
# a noun form. For nouns, we need singular and plural, and possessive for
# both singular and plural.

# Because most verbs have multiple present tenses depending on the subject,
# and because some nouns are also verbs, we choose to represent the present
# tense as any of them (eg. both "discard" and "discards" map to the DISCARD
# token), and the noun tokens represent both singular and plural noun forms.

# Note that the way this is done will make the language much wider than
# necessary, allowing strange constructions like "you discards" or
# "pays a first strike cost". This is okay since we don't need to be strict
# given that we have a finite (albeit regularly increasing) card pool, and
# our objective is not to disallow poorly worded Magic cards but to interpret
# all existing Magic cards.

# Some keywords are technically multiple words, such as "first strike" and
# "cumulative upkeep". For lexing clarity, these are tokenized separately
# if the first word appears elsewhere in Magic's vocabulary. Hence "first
# strike" will be split into "first" and "strike" while "cumulative upkeep"
# will not be split at all.

class Keyword(object):
    """ Common superclass for the types of words that are used here.
        Allows export of a mini-dictionary that contains words and tokens. """
    def __init__(self, *tokenlists):
        """ Each element of tokenlists should be a list of strings
            (token, *ids) where token is a string, eg. "ACTION",
            and the rest of the list are ids, eg. ("action", "actions"). """
        self.dict = dict([(w, ts[0])
                          for ts in tokenlists if ts for w in ts[1:]])

class Verb(Keyword):
    """ All verbs must have present and past tenses.
        Others are optional. Each tense is a list, with the first
        value being the token used to represent the other words
        in the list.
        
        The noun, if provided, should be the word meaning the act of
        (this verb), and not meaning one that is the subject or predicate
        of the action. For example, "ACTIVATION" would be appropriate for
        "ACTIVATE", but "ATTACKER" would not be for "ATTACK". """
    def __init__(self, present, past, progressive=(), noun=()):
        self.type = present[0]
        self.present = present
        self.past = past
        self.progressive = progressive
        self.noun = noun
        super(Verb, self).__init__(present, past, progressive, noun)

class Noun(Keyword):
    """ Nouns are different from verbs in that only one form of a token
        is provided, and the rest are generated.
        A noun must have all four forms given as strings:
            singular, plural, singular possessive, plural possessive. """
    def __init__(self, token, singular, plural, sing_poss, pl_poss):
        self.type = token
        self.singular = singular
        self.plural = plural
        self.sing_poss = sing_poss
        self.pl_poss = pl_poss
        super(Noun, self).__init__((token, singular, plural),
                                   (token + "_POSS", sing_poss),
                                   (token + "_PL_POSS", pl_poss))

actions = {}
_actions = [
    # Player actions
    # These are actions that one can say "I <perform action>"
    # or "Whenever a player <performs action>".

    # Basic actions (mostly straightforward English meanings)
    Verb(   ("ADD", "add", "adds"),
            ("ADDED", "added"),
            ("ADDING", "adding")),
    Verb(   ("ANTE", "ante", "antes"),
            ("ANTED", "anted")),
    Verb(   ("ATTACK", "attack", "attacks"),
            ("ATTACKED", "attacked"),
            ("ATTACKING", "attacking")),
    Verb(   ("BEGIN", "begin", "begins"),
            ("BEGAN", "began")),
    Verb(   ("BID", "bid", "bids"),
            ("BID", "bid"),
            ("BIDDING", "bidding"),
            ("BIDDING", "bidding")),
    Verb(   ("BLOCK", "block", "blocks"),
            ("BLOCKED", "blocked"),
            ("BLOCKING", "blocking")),
    Verb(   ("CHANGE", "change", "changes"),
            ("CHANGED", "changed"),
            ("CHANGING", "changing")),
    Verb(   ("CHOOSE", "choose", "chooses"),
            ("CHOSE", "chose"),
            ("CHOOSING", "choosing"),
            ("CHOICE", "choice", "choices")),
    Verb(   ("CONTROL", "control", "controls"),
            ("CONTROLLED", "controlled"),
            ("CONTROLLING", "controlling")),
    Verb(   ("COUNT", "count", "counts"),
            ("COUNTED", "counted")),
    Verb(   ("DECIDE", "decide", "decides"),
            ("DECIDED", "decided"),
            ("DECIDING", "deciding"),
            ("DECISION", "decision")),
    Verb(   ("DECLARE", "declare", "declares"),
            ("DECLARED", "declared"),
            ("DECLARING", "declaring"),
            ("DECLARATION", "declaration")),
    Verb(   ("DISTRIBUTE", "distribute", "distributes"),
            ("DISTRIBUTED", "distributed"),
            ("DISTRIBUTING", "distributing"),
            ("DISTRIBUTION", "distribution")),
    Verb(   ("DIVIDE", "divide", "divides"),
            ("DIVIDED", "divided"),
            ("DIVIDING", "dividing"),
            ("DIVISION", "division")),
    Verb(   ("DO", "do", "does"),
            ("DID", "did"),
            ("DOING", "doing")),
    Verb(   ("DONT", "don't", "doesn't"),
            ("DIDNT", "didn't")),
    Verb(   ("DOUBLE", "double", "doubles"),
            ("DOUBLED", "doubled")),
    Verb(   ("DRAW", "draw", "draws"),
            ("DREW", "drew")),
    Verb(   ("EMPTY", "empty", "empties"),
            ("EMPTIED", "emptied")),
    Verb(   ("FINISH", "finish", "finishes"),
            ("FINISHED", "finished")),
    Verb(   ("FLIP", "flip", "flips"),
            ("FLIPPED", "flipped"),
            ("FLIPPING", "flipping")),
    Verb(   ("GAIN", "gain", "gains"),
            ("GAINED", "gained")),
    Verb(   ("GET", "get", "gets"),
            ("GOT", "got")),
    Verb(   ("GUESS", "guess", "guesses"),
            ("GUESSED", "guessed"),
            ("GUESSING", "guessing")),
    Verb(   ("HIDE", "hide", "hides"),
            ("HID", "hid")),
    Verb(   ("IGNORE", "ignore", "ignores"),
            ("IGNORED", "ignored")),
    Verb(   ("LOOK", "look", "looks"),
            ("LOOKED", "looked")),
    Verb(   ("LOSE", "lose", "loses"),
            ("LOST", "lost"),
            ("LOSING", "losing"),
            ("LOSS", "loss")),
    Verb(   ("MOVE", "move", "moves"),
            ("MOVED", "moved"),
            ("MOVING", "moving")),
    Verb(   ("NAME", "name", "names"),
            ("NAMED", "named")),
    Verb(   ("NOTE", "note", "notes"),
            ("NOTED", "noted")),
    Verb(   ("ORDER", "order", "orders"),
            ("ORDERED", "ordered")),
    Verb(   ("OWN", "own", "owns"),
            ("OWNED", "owned"),
            ("OWNING", "owning"),
            ("OWNERSHIP", "ownership")),
    Verb(   ("PAY", "pay", "pays"),
            ("PAID", "paid"),
            ("PAYING", "paying"),
            ("PAYMENT", "payment")),
    Verb(   ("PREVENT", "prevent", "prevents"),
            ("PREVENTED", "prevented")),
    Verb(   ("PUT", "put", "puts"),
            ("PUT", "put"),
            ("PUTTING", "putting")),
    Verb(   ("REDISTRIBUTE", "redistribute", "redistributes"),
            ("REDISTRIBUTED", "redistributed"),
            ("REDISTRIBUTING", "redistributing"),
            ("REDISTRIBUTION", "redistribution")),
    Verb(   ("REMOVE", "remove", "removes"),
            ("REMOVED", "removed"),
            ("REMOVING", "removing"),
            ("REMOVAL", "removal")),
    Verb(   ("REORDER", "reorder", "reorders"),
            ("REORDERED", "reordered")),
    Verb(   ("REPEAT", "repeat", "repeats"),
            ("REPEATED", "repeated")),
    Verb(   ("REPLACE", "replace", "replaces"),
            ("REPLACED", "replaced"),
            ("REPLACING", "replacing")),
    Verb(   ("RESELECT", "reselect", "reselects"),
            ("RESELECTED", "reselected")),
    Verb(   ("RESTART", "restart", "restarts"),
            ("RESTARTED", "restarted"),
            ("RESTARTING", "restarting")),
    Verb(   ("RETURN", "return", "returns"),
            ("RETURNED", "returned")),
    Verb(   ("SELECT", "select", "selects"),
            ("SELECTED", "selected")),
    Verb(   ("SEPARATE", "separate", "separates"),
            ("SEPARATED", "separated")),
    Verb(   ("SKIP", "skip", "skips"),
            ("SKIPPED", "skipped")),
    Verb(   ("SPEND", "spend", "spends"),
            ("SPENT", "spent")),
    Verb(   ("START", "start", "starts"),
            ("STARTED", "started"),
            ("STARTING", "starting")),
    Verb(   ("STOP", "stop", "stops"),
            ("STOPPED", "stopped")),
    Verb(   ("SWITCH", "switch", "switches"),
            ("SWITCHED", "switched")),
    Verb(   ("TAKE", "take", "takes"),
            ("TOOK", "took")),
    Verb(   ("TIE", "tie", "ties"),
            ("TIED", "tied"),
            ("TYING", "tying")),
    Verb(   ("WIN", "win", "wins"),
            ("WON", "won"),
            ("WINNING", "winning")),

    # Keyword actions
    Verb(   ("ACTIVATE", "activate", "activates"),
            ("ACTIVATED", "activated"),
            ("ACTIVATING", "activating"),
            ("ACTIVATION", "activation", "activations")),
    Verb(   ("ATTACH", "attach", "attaches"),
            ("ATTACHED", "attached"),
            ("ATTACHING", "attaching")),
    Verb(   ("CAST", "cast", "casts"),
            ("CAST", "cast"),
            ("CASTING", "casting")),
    Verb(   ("COUNTER", "counter", "counters"),
            ("COUNTERED", "countered"),
            ("COUNTERING", "countering")),
    Verb(   ("DESTROY", "destroy", "destroys"),
            ("DESTROYED", "destroyed"),
            ("DESTROYING", "destroying")),
    Verb(   ("DISCARD", "discard", "discards"),
            ("DISCARDED", "discarded"),
            ("DISCARDING", "discarding")),
    Verb(   ("EXCHANGE", "exchange", "exchanges"),
            ("EXCHANGED", "exchanged"),
            ("EXCHANGING", "exchanging"),
            ("EXCHANGE", "exchange")),
    Verb(   ("EXILE", "exile", "exiles"),
            ("EXILED", "exiled"),
            ("EXILING", "exiling")),
    Verb(   ("FIGHT", "fight", "fights"),
            ("FOUGHT", "fought")),
    Verb(   ("PLAY", "play", "plays"),
            ("PLAYED", "played"),
            ("PLAYING", "playing")),
    Verb(   ("REGENERATE", "regenerate", "regenerates"),
            ("REGENERATED", "regenerated"),
            ("REGENERATING", "regenerating"),
            ("REGENERATION", "regeneration")),
    Verb(   ("REVEAL", "reveal", "reveals"),
            ("REVEALED", "revealed"),
            ("REVEALING", "revealing")),
    Verb(   ("SACRIFICE", "sacrifice", "sacrifices"),
            ("SACRIFICED", "sacrificed"),
            ("SACRIFICING", "sacrificing")),
    Verb(   ("SEARCH", "search", "searches"),
            ("SEARCHED", "searched"),
            ("SEARCHING", "searching")),
    Verb(   ("SHUFFLE", "shuffle", "shuffles"),
            ("SHUFFLED", "shuffled"),
            ("SHUFFLING", "shuffling")),
    Verb(   ("TAP", "tap", "taps"),
            ("TAPPED", "tapped"),
            ("TAPPING", "tapping")),
    Verb(   ("UNATTACH", "unattach", "unattaches"),
            ("UNATTACHED", "unattached"),
            ("UNATTACHING", "unattaching")),
    Verb(   ("UNTAP", "untap", "untaps"),
            ("UNTAPPED", "untapped"),
            ("UNTAPPING", "untapping")),
         
    # non-core keyword actions
    Verb(   ("CLASH", "clash", "clashes"),
            ("CLASHED", "clashed"),
            ("CLASHING", "clashing"),
            ("CLASH", "clash")),
    Verb(   ("FATESEAL", "fateseal", "fateseals"),
            ("FATESEALED", "fatesealed"),
            ("FATESEALING", "fatesealing")),
    Verb(   ("PROLIFERATE", "proliferate", "proliferates"),
            ("PROLIFERATED", "proliferated"),
            ("PROLIFERATING", "proliferating"),
            ("PROLIFERATION", "proliferation")),
    Verb(   ("SCRY", "scry", "scries"),
            ("SCRIED", "scried"),
            ("SCRYING", "scrying")),
    Verb(   ("TRANSFORM", "transform", "transforms"),
            ("TRANSFORMED", "transformed")),

    # special
    Verb(   ("ABANDON", "abandon", "abandons"),
            ("ABANDONED", "abandoned"),
            ("ABANDONING", "abandoning"),
            ("ABANDONMENT", "abandonment")),
    Verb(   ("PLANESWALK", "planeswalk", "planeswalks"),
            ("PLANESWALKED", "planeswalked"),
            ("PLANESWALKING", "planeswalking")),
    Verb(   ("SET_IN_MOTION", "set in motion", "sets in motion"),
            ("SET_IN_MOTION", "set in motion"),
            ("SETTING_IN_MOTION", "setting in motion")),

    # Other (non-player) actions
    Verb(   ("AFFECT", "affect", "affects"),
            ("AFFECTED", "affected")),
    Verb(   ("APPLY", "apply", "applies"),
            ("APPLIED", "applied")),
    Verb(   ("ASSEMBLE", "assemble", "assembles"),
            ("ASSEMBLED", "assembled")),
    Verb(   ("ASSIGN", "assign", "assigns"),
            ("ASSIGNED", "assigned"),
            ("ASSIGNING", "assigning"),
            ("ASSIGNMENT", "assignment")),
    Verb(   ("BECOME", "become", "becomes"),
            ("BECAME", "became")),
    Verb(   ("CAUSE", "cause", "causes"),
            ("CAUSED", "caused")),
    Verb(   ("COME", "come", "comes"),
            ("CAME", "came")),
    Verb(   ("CONTAIN", "contain", "contains"),
            ("CONTAINED", "contained")),
    Verb(   ("CONTINUE", "continue", "continues"),
            ("CONTINUED", "continued")),
    Verb(   ("DEAL", "deal", "deals"),
            ("DEALT", "dealt"),
            ("DEALING", "dealing")),
    Verb(   ("DIE", "die", "dies"),
            ("DIED", "died")),
    Verb(   ("END", "end", "ends"),
            ("ENDED", "ended")),
    Verb(   ("ENTER", "enter", "enters"),
            ("ENTERED", "entered"),
            ("ENTERING", "entering")),
    Verb(   ("INCREASE", "increase", "increases"),
            ("INCREASED", "increased")),
    Verb(   ("LEAVE", "leave", "leaves"),
            ("LEFT", "left"),
            ("LEAVING", "leaving")),
    Verb(   ("PLACE", "place", "places"),
            ("PLACED", "placed")),
    Verb(   ("PRODUCE", "produce", "produces"),
            ("PRODUCED", "produced")),
    Verb(   ("REDUCE", "reduce", "reduces"),
            ("REDUCED", "reduced")),
    Verb(   ("REMAIN", "remain", "remains"),
            ("REMAINED", "remained")),
    Verb(   ("RESOLVE", "resolve", "resolves"),
            ("RESOLVED", "resolved"),
            ("RESOLVING", "resolving"),
            ("RESOLUTION", "resolution")),
    Verb(   ("SHARE", "share", "shares"),
            ("SHARED", "shared")),
    Verb(   ("STAND", "stand", "stands"),
            ("STOOD", "stood")),
    Verb(   ("TRIGGER", "trigger", "triggers"),
            ("TRIGGERED", "triggered")),
    Verb(   ("TURN", "turn", "turns"),
            ("TURNED", "turned")),
    Verb(   ("USE", "use", "uses"),
            ("USED", "used"),
            ("USING", "using")),

    # Connective verbs
    Keyword(("ABLE", "able")),
    Verb(   ("BE", "be"),
            ("BEEN", "been"),
            ("BEING", "being")),
    Verb(   ("CAN", "can"),
            ("COULD", "could")),
    Verb(   ("CANT", "can't", "cannot"),
            ("COULDNT", "couldn't")),
    Verb(   ("IS", "is"),
            ("WAS", "was")),
    Verb(   ("ISNT", "isn't"),
            ("WASNT", "wasn't")),
    Verb(   ("ARE", "are"),
            ("WERE", "were")),
    Verb(   ("ARENT", "aren't"),
            ("WERENT", "weren't")),
    Verb(   ("HAS", "has", "have"),
            ("HAD", "had"),
            ("HAVING", "having")),
    Verb(   ("HASNT", "hasn't", "haven't"),
            ("HADNT", "hadn't")),
    Keyword(("MAY", "may")),
]
for action in _actions:
    actions.update(action.dict)

abilities = {}
_abilities = [
    # core
    Keyword(("DEATHTOUCH", "deathtouch")),
    Keyword(("DEFENDER", "defender")),
    # Double strike, first strike
    Keyword(("STRIKE", "strike")),
    # We use Verbs to describe keywords that can be used like actions
    # though they aren't officially keyword actions.
    # This allows us to define words like "kicked" here with the
    # relevant keyword.
    Verb(   ("ENCHANT", "enchant", "enchants"),
            ("ENCHANTED", "enchanted"),
            ("ENCHANTING", "enchanting")),
    Verb(   ("EQUIP", "equip", "equips"),
            ("EQUIPPED", "equipped"),
            ("EQUIPPING", "equipping")),
    Keyword(("FLASH", "flash")),
    Keyword(("FLYING", "flying")),
    Keyword(("HASTE", "haste")),
    Keyword(("HEXPROOF", "hexproof")),
    Keyword(("INTIMIDATE", "intimidate")),
    Keyword(("LANDWALK", "landwalk")),
    Keyword(("LIFELINK", "lifelink")),
    Keyword(("PROTECTION", "protection")),
    Keyword(("REACH", "reach")),
    Keyword(("SHROUD", "shroud")),
    Verb(   ("TRAMPLE", "trample", "tramples"),
            ("TRAMPLED", "trampled"),
            ("TRAMPLING", "trampling")),
    Keyword(("VIGILANCE", "vigilance")),

    # set/block-specific "expert level expansions"
    Verb(   ("ABSORB", "absorb", "absorbs"),
            ("ABSORBED", "absorbed"),
            ("ABSORBING", "absorbing")),
    Keyword(("AFFINITY", "affinity")),
    Verb(   ("AMPLIFY", "amplify", "amplifies"),
            ("AMPLIFIED", "amplified")),
    Keyword(("ANNIHILATOR", "annihilator")),
    # Aura swap
    Verb(   ("SWAP", "swap", "swaps"),
            ("SWAPPED", "swapped")),
    Keyword(("BATTLE_CRY", "battle cry")),
    Keyword(("BLOODTHIRST", "bloodthirst")),
    Keyword(("BUSHIDO", "bushido")),
    Keyword(("BUYBACK", "buyback")),
    Keyword(("CASCADE", "cascade")),
    Verb(   ("CHAMPION", "champion", "champions"),
            ("CHAMPIONED", "championed")),
    Keyword(("CHANGELING", "changeling")),
    Verb(   ("CONSPIRE", "conspire", "conspires"),
            ("CONSPIRED", "conspired")),
    Keyword(("CONVOKE", "convoke")),
    Keyword(("CUMULATIVE_UPKEEP", "cumulative upkeep")),
    Verb(   ("CYCLE", "cycle", "cycles"),
            ("CYCLED", "cycled"),
            ("CYCLING", "cycling")),
    Keyword(("DELVE", "delve")),
    Verb(   ("DEVOUR", "devour", "devours"),
            ("DEVOURED", "devoured")),
    Keyword(("DREDGE", "dredge")),
    Keyword(("ECHO", "echo")),
    Keyword(("ENTWINE", "entwine")),
    Keyword(("EPIC", "epic")),
    Verb(   ("EVOKE", "evoke", "evokes"),
            ("EVOKED", "evoked")),
    Keyword(("EXALTED", "exalted")),
    Keyword(("FADING", "fading")),
    Keyword(("FLANKING", "flanking")),
    Keyword(("FLASHBACK", "flashback")),
    Keyword(("FORECAST", "forecast")),
    Verb(   ("FORTIFY", "fortify", "fortifies"),
            ("FORTIFIED", "fortified")),
    Keyword(("FRENZY", "frenzy")),
    Verb(   ("GRAFT", "graft", "grafts"),
            ("GRAFTED", "grafted")),
    Keyword(("GRAVESTORM", "gravestorm")),
    Verb(   ("HAUNT", "haunt", "haunts"),
            ("HAUNTED", "haunted"),
            ("HAUNTING", "haunting")),
    Keyword(("HIDEAWAY", "hideaway")),
    Keyword(("HORSEMANSHIP", "horsemanship")),
    Keyword(("INFECT", "infect")),
    Keyword(("KICKER", "kicker")),
    Verb(   ("KICK", "kick", "kicks"),
            ("KICKED", "kicked")),
    # Level up
    Keyword(("LEVEL", "level")),
    Keyword(("LIVING_WEAPON", "living weapon")),
    Keyword(("MADNESS", "madness")),
    Keyword(("MODULAR", "modular")),
    Keyword(("MORPH", "morph")),
    Keyword(("MULTIKICKER", "multikicker")),
    Keyword(("NINJUTSU", "ninjutsu")),
    Keyword(("OFFERING", "offering")),
    Keyword(("PERSIST", "persist")),
    # Phasing
    Verb(   ("PHASE", "phase", "phases"),
            ("PHASED", "phased"),
            ("PHASING", "phasing")),
    Keyword(("POISONOUS", "poisonous")),
    Verb(   ("PROVOKE", "provoke", "provokes"),
            ("PROVOKED", "provoked")),
    Keyword(("PROWL", "prowl")),
    Keyword(("RAMPAGE", "rampage")),
    Keyword(("REBOUND", "rebound")),
    Verb(   ("RECOVER", "recover", "recovers"),
            ("RECOVERED", "recovered")),
    Verb(   ("REINFORCE", "reinforce", "reinforces"),
            ("REINFORCED", "reinforced")),
    Verb(   ("REPLICATE", "replicate", "replicates"),
            ("REPLICATED", "replicated")),
    Keyword(("RETRACE", "retrace")),
    Keyword(("RIPPLE", "ripple")),
    Keyword(("SHADOW", "shadow")),
    Keyword(("SOULSHIFT", "soulshift")),
    Verb(   ("SPLICE", "splice", "splices"),
            ("SPLICED", "spliced")),
    Keyword(("SPLIT_SECOND", "split second")),
    Keyword(("STORM", "storm")),
    Keyword(("SUNBURST", "sunburst")),
    Verb(   ("SUSPEND", "suspend", "suspends"),
            ("SUSPENDED", "suspended")),
    Keyword(("TOTEM_ARMOR", "totem armor")),
    Keyword(("TRANSFIGURE", "transfigure")),
    Verb(   ("TRANSMUTE", "transmute", "transmutes"),
            ("TRANSMUTED", "transmuted")),
    Keyword(("TYPECYCLING", "typecycling")),
    Verb(   ("UNEARTH", "unearth", "unearths"),
            ("UNEARTHED", "unearthed")),
    Keyword(("VANISHING", "vanishing")),
    Keyword(("WITHER", "wither")),
    # Dead
    # Banding and Bands with other
    Verb(   ("BAND", "band", "bands"),
            ("BANDED", "banded"),
            ("BANDING", "banding")),
    Keyword(("FEAR", "fear")),
]
for ability in _abilities:
    abilities.update(ability.dict)

# These have no rules meaning but may show up in text.
ability_words = {}
_ability_words = [
    Keyword(("CHANNEL", "channel")),
    Keyword(("CHROMA", "chroma")),
    Keyword(("DOMAIN", "domain")),
    Keyword(("GRANDEUR", "grandeur")),
    Keyword(("HELLBENT", "hellbent")),
    Keyword(("IMPRINT", "imprint")),
    Keyword(("JOIN_FORCES", "join forces")),
    Keyword(("KINSHIP", "kinship")),
    Keyword(("LANDFALL", "landfall")),
    Keyword(("METALCRAFT", "metalcraft")),
    Keyword(("MORBID", "morbid")),
    Keyword(("RADIANCE", "radiance")),
    Keyword(("SWEEP", "sweep")),
    Keyword(("THRESHOLD", "threshold")),
]
for aword in _ability_words:
    ability_words.update(aword.dict)

# Object, player, and card types
types = {}
_types = [
    Noun("TYPE", "type", "types", "type's", "types'"),
    Noun("SUPERTYPE", "supertype", "supertypes", "supertype's", "supertypes'"),
    Noun("SUBTYPE", "subtype", "subtypes", "subtype's", "subtypes'"),
    Noun("OBJECT", "object", "objects", "object's", "objects'"),
    Noun("ABILITY", "ability", "abilities", "ability's", "abilities'"),
    Noun("CARD", "card", "cards", "card's", "cards'"),
    Noun("COPY", "copy", "copies", "copy's", "copies'"),
    Noun("COUNTER", "counter", "counters", "counter's", "counters'"),
    Noun("EFFECT", "effect", "effects", "effect's", "effects'"),
    Noun("PERMANENT", "permanent", "permanents", "permanent's", "permanents'"),
    Noun("SOURCE", "source", "sources", "source's", "sources'"),
    Noun("SPELL", "spell", "spells", "spell's", "spells'"),
    Noun("TOKEN", "token", "tokens", "token's", "tokens'"),

    # Card Types
    Noun("ARTIFACT", "artifact", "artifacts", "artifact's", "artifacts'"),
    Noun("CREATURE", "creature", "creatures", "creature's", "creatures'"),
    Noun("ENCHANTMENT", "enchantment", "enchantments",
                        "enchantment's", "enchantments'"),
    Noun("INSTANT", "instant", "instants", "instant's", "instants'"),
    Noun("LAND", "land", "lands", "land's", "lands'"),
    Noun("PLANESWALKER", "planeswalker", "planeswalkers",
                         "planeswalker's", "planeswalkers'"),
    Noun("SORCERY", "sorcery", "sorceries", "sorcery's", "sorceries'"),
    Noun("TRIBAL", "tribal", "tribals", "tribal's", "tribals'"),

    # Player types
    Noun("PLAYER", "player", "players", "player's", "players'"),
    Noun("TEAMMATE", "teammate", "teammates", "teammate's", "teammates'"),
    Noun("OPPONENT", "opponent", "opponents", "opponent's", "opponents'"),
    Noun("CONTROLLER", "controller", "controllers",
                       "controller's", "controllers'"),
    Noun("OWNER", "owner", "owners", "owner's", "owners'"),
    Noun("BIDDER", "bidder", "bidders", "bidder's", "bidders'"),
    Keyword(("ACTIVE", "active")),
    Keyword(("ATTACKING", "attacking")),
    Keyword(("DEFENDING", "defending")),

    # Mana and Color Types
    Noun("MANA", "mana", "mana", "mana's", "mana's"),
    Noun("COLOR", "color", "colors", "color's", "colors'"),
    Keyword(("WHITE", "white")),
    Keyword(("BLUE", "blue")),
    Keyword(("BLACK", "black")),
    Keyword(("RED", "red")),
    Keyword(("GREEN", "green")),
    Keyword(("COLORLESS", "colorless")),
    Keyword(("COLORED", "colored")),
    Keyword(("MONOCOLORED", "monocolored")),
    Keyword(("MULTICOLORED", "multicolored")),

    # Other Types
    Noun("COMMANDER", "commander", "commanders", "commander's", "commanders'"),
    Noun("EMBLEM", "emblem", "emblems", "emblem's", "emblems'"),
    Noun("PLANE", "plane", "planes", "plane's", "planes'"),
    Noun("SCHEME", "scheme", "schemes", "scheme's", "schemes'"),
    Noun("VANGUARD", "vanguard", "vanguards", "vanguard's", "vanguards'"),

    # Supertypes
    Keyword(("BASIC", "basic")),
    Keyword(("LEGENDARY", "legendary")),
    Keyword(("SNOW", "snow")),
    Keyword(("WORLD", "world")),
    Keyword(("ONGOING", "ongoing")),
]
for t in _types:
    types.update(t.dict)

# Subtypes (generally nouns)
_artifact_types = [
    Noun("CONTRAPTION", "contraption", "contraptions",
                        "contraption's", "contraptions'"),
    Noun("EQUIPMENT", "equipment", "equipment", "equipment's", "equipment's"),
    Noun("FORTIFICATION", "fortification", "fortifications",
                          "fortification's", "fortifications'"),
]

_enchantment_types = [
    Noun("AURA", "aura", "auras", "aura's", "auras'"),
    Noun("CURSE", "curse", "curses", "curse's", "curses'"),
    Noun("SHRINE", "shrine", "shrines", "shrine's", "shrines'"),
]

_land_types = [
    Noun("DESERT", "desert", "deserts", "desert's", "deserts'"),
    Noun("FOREST", "forest", "forests", "forest's", "forests'"),
    Noun("ISLAND", "island", "islands", "island's", "islands'"),
    Noun("LAIR", "lair", "lairs", "lair's", "lairs'"),
    Noun("LOCUS", "locus", "loci", "locus's", "loci's"),
    Noun("MINE", "mine", "mines", "mine's", "mines'"),
    Noun("MOUNTAIN", "mountain", "mountains", "mountain's", "mountains'"),
    Noun("PLAINS", "plains", "plains", "plains's", "plains'"),
    Noun("POWER_PLANT", "power-plant", "power-plants",
                        "power-plant's", "power-plants'"),
    Noun("SWAMP", "swamp", "swamps", "swamp's", "swamps'"),
    Noun("TOWER", "tower", "towers", "tower's", "towers'"),
    Keyword(("URZAS", "urza's")),
]

_planeswalker_types = [
    Keyword(("AJANI", "ajani")),
    Keyword(("BOLAS", "bolas")),
    Keyword(("CHANDRA", "chandra")),
    Keyword(("ELSPETH", "elspeth")),
    Keyword(("GARRUK", "garruk")),
    Keyword(("GIDEON", "gideon")),
    Keyword(("JACE", "jace")),
    Keyword(("KARN", "karn")),
    Keyword(("KOTH", "koth")),
    Keyword(("LILIANA", "liliana")),
    Keyword(("NISSA", "nissa")),
    Keyword(("SARKHAN", "sarkhan")),
    Keyword(("SORIN", "sorin")),
    Keyword(("TEZZERET", "tezzeret")),
    Keyword(("VENSER", "venser")),
]

_spell_types = [
    Keyword(("ARCANE", "arcane")),
    Noun("TRAP", "trap", "traps", "trap's", "traps'"),
]

_creature_types = [
    Noun("ADVISOR", "advisor", "advisors", "advisor's", "advisors'"),
    Noun("ALLY", "ally", "allies", "ally's", "allies'"),
    Noun("ANGEL", "angel", "angels", "angel's", "angels'"),
    Noun("ANTEATER", "anteater", "anteaters", "anteater's", "anteaters'"),
    Noun("ANTELOPE", "antelope", "antelopes", "antelope's", "antelopes'"),
    Noun("APE", "ape", "apes", "ape's", "apes'"),
    Noun("ARCHER", "archer", "archers", "archer's", "archers'"),
    Noun("ARCHON", "archon", "archons", "archon's", "archons'"),
    Noun("ARTIFICER", "artificer", "artificers", "artificer's", "artificers'"),
    Noun("ASSASSIN", "assassin", "assassins", "assassin's", "assassins'"),
    Noun("ASSEMBLY_WORKER", "assembly-worker", "assembly-workers",
                            "assembly-worker's", "assembly-workers'"),
    Noun("ATOG", "atog", "atogs", "atog's", "atogs'"),
    Noun("AUROCHS", "aurochs", "aurochs", "aurochs's", "aurochs'"),
    Noun("AVATAR", "avatar", "avatars", "avatar's", "avatars'"),
    Noun("BADGER", "badger", "badgers", "badger's", "badgers'"),
    Noun("BARBARIAN", "barbarian", "barbarians", "barbarian's", "barbarians'"),
    Noun("BASILISK", "basilisk", "basilisks", "basilisk's", "basilisks'"),
    Noun("BAT", "bat", "bats", "bat's", "bats'"),
    Noun("BEAR", "bear", "bears", "bear's", "bears'"),
    Noun("BEAST", "beast", "beasts", "beast's", "beasts'"),
    Noun("BEEBLE", "beeble", "beebles", "beeble's", "beebles'"),
    Noun("BERSERKER", "berserker", "berserkers", "berserker's", "berserkers'"),
    Noun("BIRD", "bird", "birds", "bird's", "birds'"),
    Noun("BLINKMOTH", "blinkmoth", "blinkmoths", "blinkmoth's", "blinkmoths'"),
    Noun("BOAR", "boar", "boars", "boar's", "boars'"),
    Noun("BRINGER", "bringer", "bringers", "bringer's", "bringers'"),
    Noun("BRUSHWAGG", "brushwagg", "brushwaggs", "brushwagg's", "brushwaggs'"),
    Noun("CAMARID", "camarid", "camarids", "camarid's", "camarids'"),
    Noun("CAMEL", "camel", "camels", "camel's", "camels'"),
    Noun("CARIBOU", "caribou", "caribou", "caribou's", "caribou's"),
    Noun("CARRIER", "carrier", "carriers", "carrier's", "carriers'"),
    Noun("CAT", "cat", "cats", "cat's", "cats'"),
    Noun("CENTAUR", "centaur", "centaurs", "centaur's", "centaurs'"),
    Noun("CEPHALID", "cephalid", "cephalids", "cephalid's", "cephalids'"),
    Noun("CHIMERA", "chimera", "chimeras", "chimera's", "chimeras'"),
    Noun("CITIZEN", "citizen", "citizens", "citizen's", "citizens'"),
    Noun("CLERIC", "cleric", "clerics", "cleric's", "clerics'"),
    Noun("COCKATRICE", "cockatrice", "cockatrices",
                       "cockatrice's", "cockatrices'"),
    Noun("CONSTRUCT", "construct", "constructs", "construct's", "constructs'"),
    Noun("COWARD", "coward", "cowards", "coward's", "cowards'"),
    Noun("CRAB", "crab", "crabs", "crab's", "crabs'"),
    Noun("CROCODILE", "crocodile", "crocodiles", "crocodile's", "crocodiles'"),
    Noun("CYCLOPS", "cyclops", "cyclops", "cyclops's", "cyclops'"),
    Noun("DAUTHI", "dauthi", "dauthis", "dauthi's", "dauthis'"),
    Noun("DEMON", "demon", "demons", "demon's", "demons'"),
    Noun("DESERTER", "deserter", "deserters", "deserter's", "deserters'"),
    Noun("DEVIL", "devil", "devils", "devil's", "devils'"),
    Noun("DJINN", "djinn", "djinns", "djinn's", "djinns'"),
    Noun("DRAGON", "dragon", "dragons", "dragon's", "dragons'"),
    Noun("DRAKE", "drake", "drakes", "drake's", "drakes'"),
    Noun("DREADNOUGHT", "dreadnought", "dreadnoughts",
                        "dreadnought's", "dreadnoughts'"),
    Noun("DRONE", "drone", "drones", "drone's", "drones'"),
    Noun("DRUID", "druid", "druids", "druid's", "druids'"),
    Noun("DRYAD", "dryad", "dryads", "dryad's", "dryads'"),
    Noun("DWARF", "dwarf", "dwarves", "dwarf's", "dwarves'"),
    Noun("EFREET", "efreet", "efreets", "efreet's", "efreets'"),
    Noun("ELDER", "elder", "elders", "elder's", "elders'"),
    Noun("ELDRAZI", "eldrazi", "eldrazis", "eldrazi's", "eldrazis'"),
    Noun("ELEMENTAL", "elemental", "elementals", "elemental's", "elementals'"),
    Noun("ELEPHANT", "elephant", "elephants", "elephant's", "elephants'"),
    Noun("ELF", "elf", "elves", "elf's", "elves'"),
    Noun("ELK", "elk", "elks", "elk's", "elks'"),
    Noun("EYE", "eye", "eyes", "eye's", "eyes'"),
    Noun("FAERIE", "faerie", "faeries", "faerie's", "faeries'"),
    Noun("FERRET", "ferret", "ferrets", "ferret's", "ferrets'"),
    Noun("FISH", "fish", "fish", "fish's", "fish's"),
    Noun("FLAGBEARER", "flagbearer", "flagbearers",
                       "flagbearer's", "flagbearers'"),
    Noun("FOX", "fox", "foxes", "fox's", "foxes'"),
    Noun("FROG", "frog", "frogs", "frog's", "frogs'"),
    Noun("FUNGUS", "fungus", "fungi", "fungus's", "fungi's"),
    Noun("GARGOYLE", "gargoyle", "gargoyles", "gargoyle's", "gargoyles'"),
    Noun("GERM", "germ", "germs", "germ's", "germs'"),
    Noun("GIANT", "giant", "giants", "giant's", "giants'"),
    Noun("GNOME", "gnome", "gnomes", "gnome's", "gnomes'"),
    Noun("GOAT", "goat", "goats", "goat's", "goats'"),
    Noun("GOBLIN", "goblin", "goblins", "goblin's", "goblins'"),
    Noun("GOLEM", "golem", "golems", "golem's", "golems'"),
    Noun("GORGON", "gorgon", "gorgons", "gorgon's", "gorgons'"),
    Noun("GRAVEBORN", "graveborn", "graveborns", "graveborn's", "graveborns'"),
    Noun("GREMLIN", "gremlin", "gremlins", "gremlin's", "gremlins'"),
    Noun("GRIFFIN", "griffin", "griffins", "griffin's", "griffins'"),
    Noun("HAG", "hag", "hags", "hag's", "hags'"),
    Noun("HARPY", "harpy", "harpies", "harpy's", "harpies'"),
    Noun("HELLION", "hellion", "hellions", "hellion's", "hellions'"),
    Noun("HIPPO", "hippo", "hippos", "hippo's", "hippos'"),
    Noun("HIPPOGRIFF", "hippogriff", "hippogriffs",
                       "hippogriff's", "hippogriffs'"),
    Noun("HOMARID", "homarid", "homarids", "homarid's", "homarids'"),
    Noun("HOMUNCULUS", "homunculus", "homunculi",
                       "homunculus's", "homunculi's"),
    Noun("HORROR", "horror", "horrors", "horror's", "horrors'"),
    Noun("HORSE", "horse", "horses", "horse's", "horses'"),
    Noun("HOUND", "hound", "hounds", "hound's", "hounds'"),
    Noun("HUMAN", "human", "humans", "human's", "humans'"),
    Noun("HYDRA", "hydra", "hydras", "hydra's", "hydras'"),
    Noun("HYENA", "hyena", "hyenas", "hyena's", "hyenas'"),
    Noun("ILLUSION", "illusion", "illusions", "illusion's", "illusions'"),
    Noun("IMP", "imp", "imps", "imp's", "imps'"),
    Noun("INCARNATION", "incarnation", "incarnations",
                        "incarnation's", "incarnations'"),
    Noun("INSECT", "insect", "insects", "insect's", "insects'"),
    Noun("JELLYFISH", "jellyfish", "jellyfish", "jellyfish's", "jellyfish's"),
    Noun("JUGGERNAUT", "juggernaut", "juggernauts",
                       "juggernaut's", "juggernauts'"),
    Noun("KAVU", "kavu", "kavus", "kavu's", "kavus'"),
    Noun("KIRIN", "kirin", "kirins", "kirin's", "kirins'"),
    Noun("KITHKIN", "kithkin", "kithkins", "kithkin's", "kithkins'"),
    Noun("KNIGHT", "knight", "knights", "knight's", "knights'"),
    Noun("KOBOLD", "kobold", "kobolds", "kobold's", "kobolds'"),
    Noun("KOR", "kor", "kors", "kor's", "kors'"),
    Noun("KRAKEN", "kraken", "kraken", "kraken's", "kraken's"),
    Noun("LAMMASU", "lammasu", "lammasu", "lammasu's", "lammasu's"),
    Noun("LEECH", "leech", "leeches", "leech's", "leeches'"),
    Noun("LEVIATHAN", "leviathan", "leviathans", "leviathan's", "leviathans'"),
    # See Anthony Alongi, Serious Fun, July 08, 2003, mtgcom/daily/aa79
    Noun("LHURGOYF", "lhurgoyf", "lhurgoyfu", "lhurgoyf's", "lhurgoyfu's"),
    Noun("LICID", "licid", "licids", "licid's", "licids'"),
    Noun("LIZARD", "lizard", "lizards", "lizard's", "lizards'"),
    Noun("MANTICORE", "manticore", "manticores", "manticore's", "manticores'"),
    Noun("MASTICORE", "masticore", "masticores", "masticore's", "masticores'"),
    Noun("MERCENARY", "mercenary", "mercenaries",
                      "mercenary's", "mercenaries'"),
    Noun("MERFOLK", "merfolk", "merfolk", "merfolk's", "merfolk's"),
    Noun("METATHRAN", "metathran", "metathrans", "metathran's", "metathrans'"),
    Noun("MINION", "minion", "minions", "minion's", "minions'"),
    Noun("MINOTAUR", "minotaur", "minotaurs", "minotaur's", "minotaurs'"),
    Noun("MONGER", "monger", "mongers", "monger's", "mongers'"),
    Noun("MONGOOSE", "mongoose", "mongooses", "mongoose's", "mongooses'"),
    Noun("MONK", "monk", "monks", "monk's", "monks'"),
    Noun("MOONFOLK", "moonfolk", "moonfolk", "moonfolk's", "moonfolk's"),
    Noun("MUTANT", "mutant", "mutants", "mutant's", "mutants'"),
    Noun("MYR", "myr", "myrs", "myr's", "myrs'"),
    Noun("MYSTIC", "mystic", "mystics", "mystic's", "mystics'"),
    Noun("NAUTILUS", "nautilus", "nautiluses", "nautilus's", "nautiluses'"),
    Noun("NEPHILIM", "nephilim", "nephilims", "nephilim's", "nephilims'"),
    Noun("NIGHTMARE", "nightmare", "nightmares", "nightmare's", "nightmares'"),
    Noun("NIGHTSTALKER", "nightstalker", "nightstalkers",
                         "nightstalker's", "nightstalkers'"),
    Noun("NINJA", "ninja", "ninjas", "ninja's", "ninjas'"),
    Noun("NOGGLE", "noggle", "noggles", "noggle's", "noggles'"),
    Noun("NOMAD", "nomad", "nomads", "nomad's", "nomads'"),
    Noun("OCTOPUS", "octopus", "octopi", "octopus's", "octopi's"),
    Noun("OGRE", "ogre", "ogres", "ogre's", "ogres'"),
    Noun("OOZE", "ooze", "oozes", "ooze's", "oozes'"),
    Noun("ORB", "orb", "orbs", "orb's", "orbs'"),
    Noun("ORC", "orc", "orcs", "orc's", "orcs'"),
    Noun("ORGG", "orgg", "orggs", "orgg's", "orggs'"),
    Noun("OUPHE", "ouphe", "ouphes", "ouphe's", "ouphes'"),
    Noun("OX", "ox", "oxen", "ox's", "oxen's"),
    Noun("OYSTER", "oyster", "oysters", "oyster's", "oysters'"),
    Noun("PEGASUS", "pegasus", "pegasus", "pegasus's", "pegasus's"),
    Noun("PENTAVITE", "pentavite", "pentavites", "pentavite's", "pentavites'"),
    Noun("PEST", "pest", "pests", "pest's", "pests'"),
    Noun("PHELDDAGRIF", "phelddagrif", "phelddagrifs",
                        "phelddagrif's", "phelddagrifs'"),
    Noun("PHOENIX", "phoenix", "phoenix", "phoenix's", "phoenix's"),
    Noun("PINCHER", "pincher", "pinchers", "pincher's", "pinchers'"),
    Noun("PIRATE", "pirate", "pirates", "pirate's", "pirates'"),
    Noun("PLANT", "plant", "plants", "plant's", "plants'"),
    Noun("PRAETOR", "praetor", "praetors", "praetor's", "praetors'"),
    Noun("PRISM", "prism", "prisms", "prism's", "prisms'"),
    Noun("RABBIT", "rabbit", "rabbits", "rabbit's", "rabbits'"),
    Noun("RAT", "rat", "rats", "rat's", "rats'"),
    Noun("REBEL", "rebel", "rebels", "rebel's", "rebels'"),
    Noun("REFLECTION", "reflection", "reflections",
                       "reflection's", "reflections'"),
    Noun("RHINO", "rhino", "rhinos", "rhino's", "rhinos'"),
    Noun("RIGGER", "rigger", "riggers", "rigger's", "riggers'"),
    Noun("ROGUE", "rogue", "rogues", "rogue's", "rogues'"),
    Noun("SALAMANDER", "salamander", "salamanders",
                       "salamander's", "salamanders'"),
    Noun("SAMURAI", "samurai", "samurai", "samurai's", "samurai's"),
    Noun("SAND", "sand", "sand", "sand's", "sand's"),
    Noun("SAPROLING", "saproling", "saprolings", "saproling's", "saprolings'"),
    Noun("SATYR", "satyr", "satyrs", "satyr's", "satyrs'"),
    Noun("SCARECROW", "scarecrow", "scarecrows", "scarecrow's", "scarecrows'"),
    Noun("SCORPION", "scorpion", "scorpions", "scorpion's", "scorpions'"),
    Noun("SCOUT", "scout", "scouts", "scout's", "scouts'"),
    Noun("SERF", "serf", "serfs", "serf's", "serfs'"),
    Noun("SERPENT", "serpent", "serpents", "serpent's", "serpents'"),
    Noun("SHADE", "shade", "shades", "shade's", "shades'"),
    Noun("SHAMAN", "shaman", "shamans", "shaman's", "shamans'"),
    Noun("SHAPESHIFTER", "shapeshifter", "shapeshifters",
                         "shapeshifter's", "shapeshifters'"),
    Noun("SHEEP", "sheep", "sheep", "sheep's", "sheep's"),
    Noun("SIREN", "siren", "sirens", "siren's", "sirens'"),
    Noun("SKELETON", "skeleton", "skeletons", "skeleton's", "skeletons'"),
    Noun("SLITH", "slith", "sliths", "slith's", "sliths'"),
    Noun("SLIVER", "sliver", "slivers", "sliver's", "slivers'"),
    Noun("SLUG", "slug", "slugs", "slug's", "slugs'"),
    Noun("SNAKE", "snake", "snakes", "snake's", "snakes'"),
    Noun("SOLDIER", "soldier", "soldiers", "soldier's", "soldiers'"),
    Noun("SOLTARI", "soltari", "soltari", "soltari's", "soltari's"),
    Noun("SPAWN", "spawn", "spawn", "spawn's", "spawn's"),
    Noun("SPECTER", "specter", "specters", "specter's", "specters'"),
    Noun("SPELLSHAPER", "spellshaper", "spellshapers",
                        "spellshaper's", "spellshapers'"),
    Noun("SPHINX", "sphinx", "sphinx", "sphinx's", "sphinx's"),
    Noun("SPIDER", "spider", "spiders", "spider's", "spiders'"),
    Noun("SPIKE", "spike", "spikes", "spike's", "spikes'"),
    Noun("SPIRIT", "spirit", "spirits", "spirit's", "spirits'"),
    Noun("SPLINTER", "splinter", "splinters", "splinter's", "splinters'"),
    Noun("SPONGE", "sponge", "sponges", "sponge's", "sponges'"),
    Noun("SQUID", "squid", "squids", "squid's", "squids'"),
    Noun("SQUIRREL", "squirrel", "squirrels", "squirrel's", "squirrels'"),
    Noun("STARFISH", "starfish", "starfish", "starfish's", "starfish's"),
    Noun("SURRAKAR", "surrakar", "surrakars", "surrakar's", "surrakars'"),
    Noun("SURVIVOR", "survivor", "survivors", "survivor's", "survivors'"),
    Noun("TETRAVITE", "tetravite", "tetravites", "tetravite's", "tetravites'"),
    Noun("THALAKOS", "thalakos", "thalakos", "thalakos's", "thalakos'"),
    Noun("THOPTER", "thopter", "thopters", "thopter's", "thopters'"),
    Noun("THRULL", "thrull", "thrulls", "thrull's", "thrulls'"),
    Noun("TREEFOLK", "treefolk", "treefolk", "treefolk's", "treefolk's"),
    Noun("TRISKELAVITE", "triskelavite", "triskelavites",
                         "triskelavite's", "triskelavites'"),
    Noun("TROLL", "troll", "trolls", "troll's", "trolls'"),
    Noun("TURTLE", "turtle", "turtles", "turtle's", "turtles'"),
    Noun("UNICORN", "unicorn", "unicorns", "unicorn's", "unicorns'"),
    Noun("VAMPIRE", "vampire", "vampires", "vampire's", "vampires'"),
    Noun("VEDALKEN", "vedalken", "vedalkens", "vedalken's", "vedalkens'"),
    Noun("VIASHINO", "viashino", "viashinos", "viashino's", "viashinos'"),
    Noun("VOLVER", "volver", "volvers", "volver's", "volvers'"),
    Noun("WALL", "wall", "walls", "wall's", "walls'"),
    Noun("WARRIOR", "warrior", "warriors", "warrior's", "warriors'"),
    Noun("WEIRD", "weird", "weirds", "weird's", "weirds'"),
    Noun("WEREWOLF", "werewolf", "werewolves", "werewolf's", "werewolves'"),
    Noun("WHALE", "whale", "whales", "whale's", "whales'"),
    Noun("WIZARD", "wizard", "wizards", "wizard's", "wizards'"),
    Noun("WOLF", "wolf", "wolves", "wolf's", "wolves'"),
    Noun("WOLVERINE", "wolverine", "wolverines", "wolverine's", "wolverines'"),
    Noun("WOMBAT", "wombat", "wombats", "wombat's", "wombats'"),
    Noun("WORM", "worm", "worms", "worm's", "worms'"),
    Noun("WRAITH", "wraith", "wraiths", "wraith's", "wraiths'"),
    Noun("WURM", "wurm", "wurms", "wurm's", "wurms'"),
    Noun("YETI", "yeti", "yeti", "yeti's", "yeti's"),
    Noun("ZOMBIE", "zombie", "zombies", "zombie's", "zombies'"),
    Noun("ZUBERA", "zubera", "zubera", "zubera's", "zubera's"),
]

_plane_types = [
    Keyword(("ALARA", "alara")),
    Keyword(("ARKHOS", "arkhos")),
    Keyword(("BOLASS_MEDITATION_REALM", "bolas's meditation realm")),
    Keyword(("DOMINARIA", "dominaria")),
    Keyword(("EQUILOR", "equilor")),
    Keyword(("IQUATANA", "iquatana")),
    Keyword(("IR", "ir")),
    Keyword(("KALDHEIM", "kaldheim")),
    Keyword(("KAMIGAWA", "kamigawa")),
    Keyword(("KARSUS", "karsus")),
    Keyword(("LORWYN", "lorwyn")),
    Keyword(("LUVION", "luvion")),
    Keyword(("MERCADIA", "mercadia")),
    Keyword(("MIRRODIN", "mirrodin")),
    Keyword(("MOAG", "moag")),
    Keyword(("MURAGANDA", "muraganda")),
    Keyword(("PHYREXIA", "phyrexia")),
    Keyword(("PYRULEA", "pyrulea")),
    Keyword(("RABIAH", "rabiah")),
    Keyword(("RATH", "rath")),
    Keyword(("RAVNICA", "ravnica")),
    Keyword(("SEGOVIA", "segovia")),
    Keyword(("SERRAS_REALM", "serra's realm")),
    Keyword(("SHADOWMOOR", "shadowmoor")),
    Keyword(("SHANDALAR", "shandalar")),
    Keyword(("ULGROTHA", "ulgrotha")),
    Keyword(("VALLA", "valla")),
    Keyword(("WILDFIRE", "wildfire")),
    Keyword(("ZENDIKAR", "zendikar")),
]

counter_types = [
    "age",
    "aim",
    "arrow",
    "arrowhead",
    "awakening",
    "blaze",
    "blood",
    "bounty",
    "bribery",
    "carrion",
    "charge",
    "corpse",
    "credit",
    "cube",
    "currency",
    "death",
    "delay",
    "depletion",
    "devotion",
    "divinity",
    "doom",
    "dream",
    "echo",
    "elixir",
    "energy",
    "eon",
    "fade",
    "fate",
    "feather",
    "flood",
    "fungus",
    "fuse",
    "glyph",
    "gold",
    "growth",
    "hatchling",
    "healing",
    "hoofprint",
    "hourglass",
    "hunger",
    "ice",
    "infection",
    "intervention",
    "javelin",
    "ki",
    "level",
    "luck",
    "magnet",
    "mannequin",
    "matrix",
    "mine",
    "mining",
    "mire",
    "music",
    "net",
    "omen",
    "ore",
    "page",
    "pain",
    "paralyzation",
    "petal",
    "phylactery",
    "pin",
    "plague",
    "poison",
    "polyp",
    "pressure",
    "pupa",
    "quest",
    "rust",
    "scream",
    "shell",
    "shield",
    "shred",
    "sleep",
    "sleight",
    "soot",
    "spore",
    "storage",
    "strife",
    "study",
    "theft",
    "tide",
    "time",
    "tower",
    "training",
    "trap",
    "treasure",
    "velocity",
    "verse",
    "vitality",
    "wage",
    "winch",
    "wind",
    "wish",
]

_subtypes = (_artifact_types + _creature_types + _enchantment_types
             + _land_types + _plane_types + _planeswalker_types + _spell_types)
# Mapping from a subtype word to its canonical form
subtype_lookup = {}
subtypes = []
subtypes_poss = []
for st in _subtypes:
    for word, token in st.dict.items():
        if token.endswith("_PL_POSS"):
            # We don't need to distinguish subtype plural possessive
            # from subtype singular possessive
            subtypes_poss.append(word)
            subtype_lookup[word] = token[:-8]
        elif token.endswith("_POSS"):
            subtypes_poss.append(word)
            subtype_lookup[word] = token[:-5]
        else:
            subtypes.append(word)
            subtype_lookup[word] = token

zones = {}
_zones = [
    Keyword(("BATTLEFIELD", "battlefield")),
    Keyword(("COMMAND", "command")),
    Keyword(("EXILE", "exile")),
    Noun("GRAVEYARD", "graveyard", "graveyards", "graveyard's", "graveyards'"),
    Noun("HAND", "hand", "hands", "hand's", "hands'"),
    Noun("LIBRARY", "library", "libraries", "library's", "libraries'"),
    Keyword(("STACK", "stack")),

    Noun("DECK", "deck", "decks", "deck's", "decks'"),
    Noun("GAME", "game", "games", "game's", "games'"),
    Noun("SIDEBOARD", "sideboard", "sideboards", "sideboard's", "sideboards'"),
    Noun("SUBGAME", "subgame", "subgames", "subgame's", "subgames"),
    Noun("ZONE", "zone", "zones", "zone's", "zones'"),
    Keyword(("OUTSIDE", "outside")),
    Keyword(("ANYWHERE", "anywhere")),
]
for z in _zones:
    zones.update(z.dict)

turn_structure = {}
_turn_structure = [
    Noun("TURN", "turn", "turns", "turn's", "turns'"),
    Noun("PHASE", "phase", "phases", "phase's", "phases'"),
    Noun("STEP", "step", "steps", "step's", "steps'"),

    # Phases
    Keyword(("BEGINNING", "beginning")),
    Keyword(("MAIN", "main")),
    Keyword(("PRECOMBAT", "precombat")),
    Keyword(("POSTCOMBAT", "postcombat")),
    Keyword(("COMBAT", "combat")),
    Keyword(("ENDING", "ending")),

    # Steps
    Keyword(("UNTAP", "untap")),
    Noun("UPKEEP", "upkeep", "upkeeps", "upkeep's", "upkeeps'"),
    Keyword(("DRAW", "draw")),
    Keyword(("BEGINNING", "beginning")), # of combat
    Keyword(("DECLARE", "declare")),
    Keyword(("ATTACKERS", "attackers")),
    Keyword(("BLOCKERS", "blockers")),
    Keyword(("DAMAGE", "damage")), # combat damage
    Keyword(("END", "end")), # of combat; end step
    Keyword(("CLEANUP", "cleanup")),
]
for ts in _turn_structure:
    turn_structure.update(ts.dict)

concepts = {}
_concepts = [
    # Abilities, spells, effects
    Keyword(("ADDITION", "addition")),
    Keyword(("ADDITIONAL", "additional")),
    Keyword(("CONVERTED", "converted")),
    Noun("COST", "cost", "costs", "cost's", "costs'"),
    Noun("TARGET", "target", "targets", "target's", "targets'"),

    # mana
    Keyword(("COMBINATION", "combination")),
    Noun("MANA", "mana", "mana", "mana's", "mana's"),
    Noun("POOL", "pool", "pools", "pool's", "pools'"),
    Noun("SYMBOL", "symbol", "symbols", "symbol's", "symbols'"),

    # Object or zone parts
    Noun("BOTTOM", "bottom", "bottoms", "bottom's", "bottoms'"),
    Noun("TOP", "top", "tops", "top's", "tops'"),
    Keyword(("LIFE", "life")),
    Keyword(("TOTAL", "total", "totals")),
    Keyword(("POWER", "power")),
    Keyword(("TOUGHNESS", "toughness")),
    Keyword(("TEXT", "text")),
    Keyword(("FULL", "full")),
    Noun("INSTANCE", "instance", "instances", "instance's", "instances'"),

    # numbers
    Noun("NUMBER", "number", "numbers", "number's", "numbers'"),

    # Math
    Keyword(("AMOUNT", "amount")),
    Keyword(("MINUS", "minus")),
    Keyword(("PLUS", "plus")),
    Keyword(("TIMES", "times")),
    Keyword(("TWICE", "twice")),
    Keyword(("TOTAL", "total")),
    Keyword(("VALUE", "value")),
    Keyword(("HALF", "half")),
    Keyword(("EVENLY", "evenly")),
    Verb(   ("ROUND", "round", "rounds"),
            ("ROUNDED", "rounded")),
    Keyword(("UP", "up")),
    Keyword(("DOWN", "down")),
    Keyword(("MAXIMUM", "maximum")),
    Keyword(("MINIMUM", "minimum")),

    # Limits
    Keyword(("ONCE", "once")),
    Keyword(("SINGLE", "single")),

    # Groupings
    Keyword(("EACH", "each")),
    Keyword(("EVERY", "every")),
    Keyword(("EVERYTHING", "everything")),
    Noun("PILE", "pile", "piles", "pile's", "piles'"),
    Keyword(("EVEN", "even")),
    Keyword(("ODD", "odd")),
    Keyword(("COMMON", "common")),
    Keyword(("SAME", "same")),
    Keyword(("DIFFERENT", "different")),
    Keyword(("DIFFERENCE", "difference")),
    Keyword(("KIND", "kind")),
    Keyword(("ALL", "all")),
    Keyword(("BOTH", "both")),
    Keyword(("ONLY", "only")),
    Keyword(("MANY", "many")),
    Keyword(("ANY", "any")),
    Keyword(("SOME", "some")),
    Keyword(("NONE", "none")),
    Keyword(("NO", "no")),
    Keyword(("OTHER", "other")),
    Keyword(("ANOTHER", "another")),
    Keyword(("REST", "rest")),
    Keyword(("LEFT", "left")),
    Keyword(("RIGHT", "right")),
    Keyword(("WAR", "war")),
    Keyword(("PEACE", "peace")),

    # comparisons
    Keyword(("MOST", "most")),
    Keyword(("FEWEST", "fewest")),
    Keyword(("GREATEST", "greatest")),
    Keyword(("LEAST", "least")),
    Keyword(("MORE", "more")),
    Keyword(("LESS", "less")),
    Keyword(("HIGH", "high")),
    Keyword(("LOW", "low")),
    Keyword(("HIGHER", "higher")),
    Keyword(("LOWER", "lower")),
    Keyword(("HIGHEST", "highest")),
    Keyword(("LOWEST", "lowest")),
    Keyword(("GREATER", "greater")),
    Keyword(("FEWER", "fewer")),
    Keyword(("LESSER", "lesser")),
    Keyword(("SMALLER", "smaller")),
    Keyword(("LONG", "long")),
    Keyword(("SHORT", "short")),
    Keyword(("LONGER", "longer")),
    Keyword(("SHORTER", "shorter")),
    Keyword(("THAN", "than")),
    Keyword(("DIRECTLY", "directly")),
    Keyword(("ABOVE", "above")),
    Keyword(("BELOW", "below")),
    Keyword(("OVER", "over")),
    Keyword(("UNDER", "under")),
    Keyword(("AMONG", "among")),
    Keyword(("BETWEEN", "between")),
    Keyword(("EQUAL", "equal", "equals")),
    Keyword(("EXACTLY", "exactly")),
    Keyword(("BEYOND", "beyond")),
    Keyword(("MUCH", "much")),

    # Special states and statuses
    Keyword(("ALONE", "alone")),
    Keyword(("CHOSEN", "chosen")),
    Keyword(("DRAWN", "drawn")),
    Keyword(("FACE_UP", "face-up", "face up")),
    Keyword(("FACE_DOWN", "face-down", "face down")),
    Keyword(("LABEL", "label")),
    Keyword(("LEVEL", "level")),
    Keyword(("MARKED", "marked")),
    Keyword(("ORIGINAL", "original")),
    Keyword(("PHASED_OUT", "phased-out")),
    Keyword(("POISONED", "poisoned")),
    Keyword(("INDESTRUCTIBLE", "indestructible")),
    Keyword(("TARGETED", "targeted")),
    Keyword(("UNBLOCKABLE", "unblockable")),
    Keyword(("UNBLOCKED", "unblocked")),
    Keyword(("UNCHANGED", "unchanged")),

    # Pronouns
    Keyword(("YOU", "you")),
    Keyword(("YOUR", "your", "yours")),
    Keyword(("YOU_ARE", "you're")),
    Keyword(("YOU_HAVE", "you've")),
    # Their, or his or her
    Keyword(("THEIR", "their")),
    # Them, or him or her
    Keyword(("THEM", "them")),
    # They, or he or she
    Keyword(("THEY", "they")),
    Keyword(("THEY_ARE", "they're")),
    Keyword(("ITSELF", "itself")),
    # Planeswalkers use these
    Keyword(("HE", "he")),
    Keyword(("HIM", "him")),
    Keyword(("HIMSELF", "himself")),
    Keyword(("HIS", "his")),
    Keyword(("SHE", "she")),
    Keyword(("HER", "her")),
    Keyword(("HERSELF", "herself")),

    # Hand size
    Keyword(("SIZE", "size")),

    # Damage
    Keyword(("DAMAGE", "damage")),
    Keyword(("LETHAL", "lethal")),
    Keyword(("POINT", "point")),
    Keyword(("POISON", "poison")),

    # Randomization and guessing
    Noun("COIN", "coin", "coins", "coin's", "coins'"),
    Keyword(("HEADS", "heads")),
    Keyword(("TAILS", "tails")),
    Keyword(("RANDOM", "random")),
    Keyword(("WRONG", "wrong")),

    # Special bidding
    Keyword(("BROKEN", "broken")),
    Noun("ITEM", "item", "items", "item's", "items'"),
    Keyword(("SECRETLY", "secretly")),
    Keyword(("STAKES", "stakes")),

    # Rules
    Keyword(("LEGAL", "legal")),
    Keyword(("LEGEND_RULE", "legend rule")),

    # Before the game
    Keyword(("MULLIGAN", "mulligan")),
    Keyword(("OPENING", "opening")),

    # Subgames
    Keyword(("MAGIC", "magic")),

    # Color identity (Commander)
    Keyword(("IDENTITY", "identity")),

    # Timing
    Keyword(("AFTER", "after")),
    Keyword(("AGAIN", "again")),
    Keyword(("BEFORE", "before")),
    Keyword(("CONTINUOUSLY", "continuously")),
    Keyword(("DURING", "during")),
    Keyword(("NEXT", "next")),
    Keyword(("PREVIOUSLY", "previously")),
    Keyword(("RECENT", "recent")),
    Keyword(("RECENTLY", "recently")),
    Keyword(("SIMULTANEOUSLY", "simultaneously")),
    Keyword(("SINCE", "since")),
    Keyword(("TIME", "time")),
    Keyword(("UNTIL", "until")),
    Keyword(("WHEN", "when", "whenever")),
    Keyword(("WHILE", "while")),

    # Conditions and references
    Keyword(("ALREADY", "already")),
    Keyword(("BACK", "back")),
    Keyword(("BY", "by")),
    Keyword(("ELSE", "else")),
    Keyword(("EXCEPT", "except")),
    Keyword(("FAR", "far")),
    Keyword(("FOLLOWED", "followed")),
    Keyword(("FROM", "from")),
    Keyword(("IF", "if")),
    Keyword(("IN", "in")),
    Keyword(("INSTEAD", "instead")),
    Keyword(("INTO", "into")),
    Keyword(("IT", "it")),
    Keyword(("IT_IS", "it's")),
    Keyword(("ITS", "its")),
    Keyword(("LIKEWISE", "likewise")),
    Keyword(("ON", "on")),
    Keyword(("ONTO", "onto")),
    Keyword(("OTHERWISE", "otherwise")),
    Keyword(("OUT", "out")),
    Keyword(("PROCESS", "process")),
    Keyword(("RATHER", "rather")),
    Keyword(("STILL", "still")),
    Keyword(("THAT", "that")),
    Keyword(("THAT_IS", "that's")),
    Keyword(("THERE", "there")),
    Keyword(("THERE_IS", "there's")),
    Keyword(("THIS", "this")),
    Keyword(("THOSE", "those")),
    Keyword(("THOUGH", "though")),
    Keyword(("TO", "to")),
    Keyword(("UNLESS", "unless")),
    Keyword(("WAY", "way")),
    Keyword(("WHERE", "where")),
    Keyword(("WHETHER", "whether")),
    Keyword(("WHICH", "which", "whichever")),
    Keyword(("WHO", "who")),
    Keyword(("WHOM", "whom")),
    Keyword(("WHOSE", "whose")),
    Keyword(("WOULD", "would")),

    # Expansions
    Keyword(("EXPANSION", "expansion")),
    Keyword(("ARABIAN_NIGHTS", "arabian nights")),
    Keyword(("ANTIQUITIES", "antiquities")),
    Keyword(("HOMELANDS", "homelands")),
]
for c in _concepts:
    concepts.update(c.dict)

misc_words = {}
_misc = [
    Keyword(("A", "a", "an")),
    Keyword(("ALSO", "also")),
    Keyword(("AND", "and")),
    Keyword(("AND_OR", "and/or")),
    Keyword(("AS", "as")),
    Keyword(("AT", "at")),
    Keyword(("BUT", "but")),
    Keyword(("EITHER", "either")),
    Keyword(("EXCESS", "excess")),
    Keyword(("EXTRA", "extra")),
    Keyword(("FOR", "for")),
    Keyword(("HOW", "how")),
    Keyword(("MAKE", "make")),
    Keyword(("MUST", "must")),
    Keyword(("NEW", "new")),
    Keyword(("NON", "non-")),
    Keyword(("NOT", "not")),
    Keyword(("OF", "of")),
    Keyword(("OR", "or")),
    Keyword(("PART", "part")),
    Keyword(("SO", "so")),
    Keyword(("THE", "the")),
    Keyword(("THEN", "then")),
    Keyword(("TRUE", "true")),
    Keyword(("WITH", "with")),
    Keyword(("WITHOUT", "without")),
    Noun("WORD", "word", "words", "word's", "words'"),
]
for m in _misc:
    misc_words.update(m.dict)

number_words = {
    "zero" : 0,
    "one" : 1,
    "two" : 2,
    "three" : 3,
    "four" : 4,
    "five" : 5,
    "six" : 6,
    "seven" : 7,
    "eight" : 8,
    "nine" : 9,
    "ten" : 10,
    "eleven" : 11,
    "twelve" : 12,
    "thirteen" : 13,
    "fourteen" : 14,
    "fifteen" : 15,
    "sixteen" : 16,
    "seventeen" : 17,
    "eighteen" : 18,
    "nineteen" : 19,
    "twenty" : 20,
}

ordinals = {
    "first" : 1,
    "second" : 2,
    "third" : 3,
    "fourth" : 4,
    "last" : -1,
}

all_words = {}
for d in (actions, abilities, ability_words, types, zones,
          turn_structure, concepts, misc_words):
    all_words.update(d)
for s in subtypes:
    all_words[s] = "OBJ_SUBTYPE"
for s in subtypes_poss:
    all_words[s] = "OBJ_SUBTYPE_POSS"
for c in counter_types:
    all_words[c] = c.upper()
for n in number_words:
    all_words[n] = "NUMBER_WORD"
for o in ordinals:
    all_words[o] = "ORDINAL_WORD"

def main():
    grammar = 'Keywords'
    header = [
        'lexer grammar {grammar};\n',
        '/* Keywords and misc text',
        ' *',
        ' * Autogenerated by demystify/keywords.py',
        ' * DO NOT EDIT DIRECTLY',
        ' */\n',
        'options {{',
        '    language = Python;',
        '}}\n',
        'tokens {{',
        '    {tokens};',
        '}}\n',
    ]
    all_tokens = set(all_words.values())
    # token -> (text, substitute token) list
    match_cases = {}
    for text, token in all_words.items():
        slen = len(text)
        for c in " '-/":
            if c in text:
                slen = min(slen, text.index(c))
        stoken = text[:slen].upper()
        if stoken not in match_cases:
            match_cases[stoken] = [(text, token)]
        else:
            match_cases[stoken].append((text, token))
    def reprsinglequote(s):
        if not s:
            return ''
        a = repr(s)
        if a[0] == '"':
            a = "'" + a[1:-1].replace("'", r"\'") + "'"
        return a
    import os
    filename = os.path.join(os.path.dirname(__file__), 'grammar',
                            '{}.g'.format(grammar))
    with open(filename, 'w') as f:
        f.write('\n'.join(header)
                .format(grammar=grammar,
                        tokens=';\n    '.join(sorted(all_tokens))))
        f.write('\n')
        for token, tlist in sorted(match_cases.items(),
                                   key=lambda x: (-len(x[0]), x[0])):
            if len(tlist) == 1:
                text, rtoken = tlist[0]
                if rtoken != token:
                    rt = ' {{$type = {}}}'.format(rtoken)
                else:
                    rt = ''
                f.write('{} : {}{};\n'.format(token,
                                              reprsinglequote(text), rt))
            else:
                sep = '\n  {bar:>{width}} '.format(bar='|', width=len(token))
                lines = []
                for text, rtoken in sorted(tlist,
                                           key=lambda x: (-len(x[0]), x[0])):
                    if rtoken != token:
                        lines.append('{} {{$type = {}}}'
                                     .format(reprsinglequote(text), rtoken))
                    else:
                        lines.append(reprsinglequote(text))
                f.write('{} : {};\n'.format(token, sep.join(lines)))
                    

if __name__ == "__main__":
    main()
