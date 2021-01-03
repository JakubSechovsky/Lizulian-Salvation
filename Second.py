import json


class Location:
    def __init__(self, place, opts):
        self.place = place
        self.opts = opts


class NPC:
    def __init__(self, loc, inv, talked_to1, talked_to2):
        self.loc = loc
        self.inv = inv
        self.talked_to1 = talked_to1
        self.talked_to2 = talked_to2


class Items:
    def __init__(self, sellval, healval, name, alchem_limit, chapel_limit):
        self.sellval = sellval
        self.buyval = 2*sellval
        self.healval = healval
        self.name = name
        self.alchem_limit = alchem_limit
        self.chapel_limit = chapel_limit

    def heal_user(self):
        if me.inv.get(self.name) > 0:
            me.health += self.healval
            me.inv[self.name] -= 1
            if me.health > me.max_health:
                me.health = me.max_health
            print(repr_mess("heal_succ", "r").format(self.healval, me.health))
        else:
            repr_mess("no_item", "p")


class Me:
    def __init__(self, max_health, health, loc, diff, run, on_turn, n, min_take, max_take, talking, last_loc, inv, way, name, safe):
        self.health = health
        self.loc = loc
        self.run = run
        self.on_turn = on_turn
        self.max_health = max_health
        self.diff = diff
        self.n = n
        self.max_take = max_take
        self.min_take = min_take
        self.talking = talking
        self.last_loc = last_loc
        self.inv = inv
        self.way = way
        self.name = name
        self.safe = safe

    def print_inv(self):
        inventory = []
        for g in self.inv:
            if self.inv.get(g):
                inventory.append(g)
        repr_mess("print_inv", "p")
        for g in inventory:
            print(repr_mess("inv_items", "r").format(self.inv.get(g), g))
        inventory = []

    def print_health(self): print(repr_mess("health", "r").format(self.health))

    def heal(self):
        if self.health < self.max_health:
            y = input(
                repr_mess("heal_item", "r"))
            if y in self.inv and y in heal_list:
                heal_list[y].heal_user()
            else:
                print(repr_mess("heal_opts", "r").format(
                    items_list["apple"].name, items_list["pear"].name))
        else:
            repr_mess("full_health", "p")

    def print_combat(self): repr_mess("combat", "p")

    def print_ava_locs(self):
        repr_mess("loc_opts", "p")
        for i in locs_list[self.loc].opts:
            print(i)

    def print_hint(self): repr_mess("hint", "p")

    def exit(self): self.run = False

    def choose_loc_check(self, y):
        if y in locs_list:
            self.last_loc = self.loc
            if y == "alchemist" and npcs_for_loc["alchemist"].talked_to2:
                self.loc = "alchemist3"
            elif y == "alchemist" and npcs_for_loc["alchemist"].talked_to1:
                self.loc = "alchemist2"
            elif self.loc == "prison" and not y == "village" and not npcs_for_loc["prison"].talked_to1:
                self.loc = "alb"
            else:
                self.loc = locs_list.get(self.loc).opts.get(y)
        else:
            repr_mess("invalid_opt", "p")
            self.choose_loc()

    def choose_loc(self):
        y = input(repr_mess("loc", "r"))
        if y == self.loc:
            repr_mess("in_loc", "p")
        else:
            if y in locs_list[self.loc].opts:
                self.choose_loc_check(y)
            else:
                repr_mess("invalid_loc", "p")
                for i in locs_list[self.loc].opts:
                    print(i)

    def rem_st(self, x):
        self.n -= x
        print(repr_mess("stones_removed", "r").format(x))

    def take(self):
        y = input(repr_mess("stone_number", "r"))
        try:
            y = int(y)
            if y in range(self.min_take, self.max_take + 1):
                self.rem_st(y)
            else:
                print(repr_mess("stone_limit", "r").format(
                    self.max_take, self.min_take))
                self.take()
        except ValueError:
            repr_mess("int_error", "p")
            self.take()

    def buy(self, x):
        y = input(repr_mess("buy", "r").format(
            x, items_list[x].buyval, self.inv.get("gold coin")))
        try:
            y = int(y)
            z = y*items_list[x].buyval
            if z > self.inv.get("gold coin"):
                print(repr_mess("need_gold", "r").format(x))
            else:
                self.inv["gold coin"] -= z
                self.inv[x] += y
                print(repr_mess("buy_succ", "r").format(y, x, z))
        except ValueError:
            repr_mess("int_error", "p")
            self.buy(x)

    def sell(self, x):
        y = input(repr_mess("sell", "r").format(
            self.inv.get(x), x, items_list[x].sellval, self.inv.get("gold coin")))
        try:
            y = int(y)
            if y > self.inv.get(x) or y < 0:
                print(repr_mess("no_items", "r").format(x))
                self.sell(x)
            else:
                z = y*items_list[x].sellval
                self.inv["gold coin"] += z
                self.inv[x] -= y
                print(repr_mess("sell_succ", "r").format(z, y, x))
        except ValueError:
            repr_mess("int_error", "p")
            self.sell(x)

    def choose_difficulty(self):
        self.diff = input(
            repr_mess("choose_diff", "r"))
        if self.diff == "1":
            self.inv["gold coin"] += 10
            self.inv["pear"] += 2
            repr_mess("easy", "p")
        elif self.diff == "2":
            self.inv["gold coin"] += 5
            self.inv["pear"] += 1
            repr_mess("medium", "p")
        elif self.diff == "3":
            repr_mess("hard", "p")
        else:
            try:
                int(self.diff)
                repr_mess("invalid_opt", "p")
            except ValueError:
                repr_mess("int_error", "p")
            self.choose_difficulty()

    def print_intro(self): print(repr_mess("intro", "r").format(self.name))


def repr_mess(x, way):
    with open("./mess.json", "r", encoding="utf-8") as mess_file:
        mess = json.load(mess_file)
        if way == "p":
            print(mess[x])
        else:
            return mess[x]


def repr_loc(name, key, way):
    with open("./locs.json", "r", encoding="utf-8") as locs_file:
        locs = json.load(locs_file)
        if way == "p":
            print(locs[name][key])
        else:
            return locs[name][key]


def return_char(name, key):
    with open("./characters.json", "r", encoding="utf-8") as chars_file:
        chars = json.load(chars_file)
        return chars[name][key]


def connect_locs():
    for loc in locs_list:
        locs_list.get(loc).opts["prison"] = "prison"


def load_locs():
    with open("./locs.json", "r", encoding="utf-8") as locs_file:
        locations = json.load(locs_file)
        for loc in locations:
            if not loc == "mess":
                inf = locations[loc]
                new_loc = Location(inf["place"], inf["opts"])
                locs_list[inf["place"]] = new_loc


def load_npcs():
    with open("./characters.json", "r", encoding="utf-8") as npcs_file:
        npcs = json.load(npcs_file)
        for npc in npcs:
            npc_check(npcs, npc)


def npc_check(npcs, npc):
    i = npcs[npc]
    if not npc == "me":
        if npc == "alchemist" or npc == "merchant" or npc == "Alberimus":
            new_npc = NPC(i["loc"], i["inv"],
                          i["talked_to1"], i["talked_to2"])
            npcs_for_loc[i["loc"]] = new_npc
        else:
            new_item = Items(i["sellval"], i["healval"],
                             i["name"], i["alchem_limit"], i["chapel_limit"])
            items_list[i["name"]] = new_item
            if npc == "apple" or npc == "pear":
                heal_list[i["name"]] = new_item


hostile_locs = {}
npcs_for_loc = {}
locs_list = {}
items_list = {}
heal_list = {}

me = Me(return_char("me", "max_health"), return_char("me", "health"), return_char("me", "loc"), return_char("me", "diff"), return_char("me", "run"), return_char("me", "on_turn"), return_char("me", "n"),
        return_char("me", "min_take"), return_char("me", "max_take"), return_char("me", "talking"), return_char("me", "last_loc"), return_char("me", "inv"), return_char("me", "way"), return_char("me", "name"), return_char("me", "safe"))
