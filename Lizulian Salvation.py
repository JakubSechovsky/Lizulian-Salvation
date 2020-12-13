import random
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
    def __init__(self, sellval, healval, name, alchem_limit):
        self.sellval = sellval
        self.buyval = 2*sellval
        self.healval = healval
        self.name = name
        self.alchem_limit = alchem_limit

    def heal_user(self):
        if me.inv.get(self.name) > 0:
            me.health += self.healval
            me.inv[self.name] -= 1
            if me.health > me.max_health:
                me.health = me.max_health
            print(repr_mess(15, "r").format(self.healval, me.health))
        else:
            repr_mess(16, "p")


class Me:
    def __init__(self, max_health, health, loc, diff, run, on_turn, n, min_take, max_take, talking, last_loc, inv, way, name):
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

    def print_inv(self):
        inventory = []
        for g in self.inv:
            if self.inv.get(g):
                inventory.append(g)
        repr_mess(8, "p")
        for g in inventory:
            print(repr_mess(17, "r").format(self.inv.get(g), g))
        inventory = []

    def print_health(self): print(repr_mess(19, "r").format(self.health))

    def print_loc(self): print(repr_mess(20, "r").format(self.loc))

    def heal(self):
        if self.health < self.max_health:
            y = input(
                "Type the exact name of the item you want to use for healing:\n>")
            if y in self.inv and y in heal_list:
                heal_list[y].heal_user()
            else:
                print(repr_mess(21, "r").format(
                    items_list["apple"].name, items_list["pear"].name))
        else:
            repr_mess(22, "p")

    def print_combat(self):
        for i in range(10, 14):
            repr_mess(i, "p")

    def print_ava_locs(self):
        repr_mess(24, "p")
        for i in locs_list[self.loc].opts:
            print(i)

    def print_hint(self): repr_mess(46, "p")

    def exit(self): self.run = False

    def wait(self):
        if me.loc in hostile_locs:
            fight_input(hostile_locs[me.loc], me)
        else:
            pass

    def choose_loc_check(self, y):
        if y in locs_list:
            self.last_loc = self.loc
            if y == "alchemist" and npcs_for_loc["alchemist"].talked_to2:
                self.loc = "alchemist3"
            elif y == "alchemist" and npcs_for_loc["alchemist"].talked_to1:
                self.loc = "alchemist2"
            elif me.loc == "prison" and not y == "village" and not npcs_for_loc["prison"].talked_to1:
                self.loc = "prisontalk"
            else:
                self.loc = locs_list.get(self.loc).opts.get(y)
        else:
            repr_mess(23, "p")
            self.choose_loc()

    def choose_loc(self):
        y = input("Type in the exact name of the location you want to go to: \n> ")
        if y == self.loc:
            repr_mess(44, "p")
        else:
            if y in locs_list[self.loc].opts:
                self.choose_loc_check(y)
            else:
                repr_mess(24, "p")
                for i in locs_list[self.loc].opts:
                    print(i)

    def rem_st(self, x):
        self.n -= x
        print(repr_mess(25, "r").format(x))

    def take(self):
        y = input("How many stones do you want to remove?\n> ")
        try:
            y = int(y)
            if y in range(me.min_take, me.max_take + 1):
                me.rem_st(y)
            else:
                print(repr_mess(37, "r").format(me.max_take, me.min_take))
                self.take()
        except ValueError:
            print("Enter an integer please.")
            self.take()

    def buy(self, x):
        y = input("How many {}s do you want to {}? (One costs {} coins)\n> ".format(
            x, self.way, items_list[x].buyval))
        try:
            y = int(y)
            z = y*items_list[x].buyval
            if z > self.inv.get("gold coin"):
                print("You require more gold for this amount of {}s.".format(x))
            else:
                self.inv["gold coin"] -= z
                self.inv[x] += y
                print("You have bought {} {}(s) for {} gold.".format(y, x, z))
        except ValueError:
            print("Enter an integer please.")
            self.buy(x)

    def sell(self, x):
        y = input("You have {} {}(s), how many do you want to sell? (One sells for {} coins)\n> ".format(
            self.inv.get(x), x, items_list[x].sellval))
        try:
            y = int(y)
            if y > self.inv.get(x) or y < 0:
                print("Enter an integer please.")
                self.sell(x)
            else:
                z = y*items_list[x].sellval
                self.inv["gold coin"] += z
                self.inv[x] -= y
                print("You gained {} coins by selling {} {}(s)".format(z, y, x))
        except ValueError:
            print("Enter an integer please.")
            self.sell(x)

    def buy_sell(self):
        x = input("What do you want to {}?\n> ".format(self.way))
        if x in self.inv:
            if x == "Shard of Alberimus" or x == "Zandalar's staff":
                print("This item is not {}able".format(self.way))
            else:
                if self.way == "buy":
                    self.buy(x)
                elif self.way == "sell" and self.inv.get(x) > 0:
                    self.sell(x)
                else:
                    repr_mess(16, "p")
        else:
            repr_mess(41, "p")
        cont_trading()


class Enemy:
    def __init__(self, loc, loot, name, chance, harm, low_limit, up_limit):
        self.loot = loot
        self.loc = loc
        self.name = name
        self.chance = chance
        self.harm = harm
        self.low_limit = low_limit
        self.up_limit = up_limit

    def simulationAI(self):
        best_act = -1
        best_score = -float("inf")
        for x in range(me.min_take, me.max_take + 1):
            act_score = 0
            for _ in range(1000):
                stone_count = me.n - x
                i_play = False
                while stone_count > 0:
                    stone_count -= min(stone_count,
                                       random.randint(me.min_take, me.max_take + 1))
                    i_play = not i_play
                if i_play:
                    act_score -= 1
                else:
                    act_score += 1
            if act_score > best_score:
                best_score = act_score
                best_act = x
        return best_act

    def perfectAI(self):
        l_nums = set([0])
        w_nums = set([])
        for x in range(2, me.n + 1):
            for i in range(me.min_take, me.max_take + 1):
                if x - i in l_nums:
                    w_nums.add(x)
            if x not in w_nums:
                l_nums.add(x)
        for i in range(me.min_take, me.max_take + 1):
            if me.n - i in l_nums:
                return(i)
        return self.simulationAI()

    def randomAI(self): return random.randint(me.min_take, me.max_take)

    def trophy(self):
        ran = random.randint(self.low_limit, self.up_limit)
        if ran == 0:
            repr_mess(45, "p")
        else:
            trophy = []
            trophy.append(ran)
            trophy.append(self.loot)
            print(repr_mess(27, "r").format(trophy[0], trophy[1]))
            x = input(
                "What do you want to do with the loot?\n1. Accept\n2.Reject\n> ")
            if x == "1":
                me.inv[self.loot] += ran
                print(repr_mess(28, "r").format(trophy[0], trophy[1]))
            elif x == "2":
                print(repr_mess(29, "r").format(trophy[0], trophy[1]))
            else:
                repr_mess(30, "p")
                self.trophy()
            trophy.clear()

    def take(self):
        if not me.inv.get("Zandalar's staff") > 0:
            ai = {"1": self.randomAI, "2": self.simulationAI,
                  "3": self.simulationAI}
            x = ai[me.diff]()
        else:
            x = self.perfectAI()
        print(repr_mess(40, "r").format(self.name, x))
        return x


def buy_or_sell():
    x = input("What do you want to do?\nEnter 1 to buy\nEnter 2 to sell\n> ")
    if x == "1":
        me.way = "buy"
    elif x == "2":
        me.way = "sell"
    else:
        repr_mess(41, "p")
        buy_or_sell()


def cont_trading():
    x = input(
        "Do you want to continue trading?\nEnter 1 to keep trading\nEnter 2 to leave the merchant [exit trading]\n> ")
    if x == "1":
        trade(npcs_for_loc[me.loc])
    elif x == "2":
        me.loc = "village"
        me.talking = False
    else:
        cont_trading()


def repr_mess(x, way):
    with open("./mess.json", "r", encoding="utf-8") as mess_file:
        mess = json.load(mess_file)
        if way == "p":
            print(mess[str(x)])
        else:
            return mess[str(x)]


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


def load_enms():
    with open("./enms.json", "r", encoding="utf-8") as enms_file:
        enms = json.load(enms_file)
        for enm in enms:
            atts = enms[enm]
            new_enm = Enemy(atts["loc"], atts["loot"], atts["name"],
                            atts["chance"], atts["harm"], atts["low_limit"], atts["up_limit"])
            hostile_locs[atts["loc"]] = new_enm


def load_locs():
    with open("./locs.json", "r", encoding="utf-8") as locs_file:
        locations = json.load(locs_file)
        for loc in locations:
            if loc == "mess":
                pass
            else:
                inf = locations[loc]
                new_loc = Location(inf["place"], inf["opts"])
                locs_list[inf["place"]] = new_loc


def load_npcs():
    with open("./characters.json", "r", encoding="utf-8") as npcs_file:
        npcs = json.load(npcs_file)
        for npc in npcs:
            i = npcs[npc]
            if npc == "me":
                pass
            elif npc == "alchemist" or npc == "merchant" or npc == "Alberimus":
                new_npc = NPC(i["loc"], i["inv"],
                              i["talked_to1"], i["talked_to2"])
                npcs_for_loc[i["loc"]] = new_npc
            else:
                new_item = Items(i["sellval"], i["healval"],
                                 i["name"], i["alchem_limit"])
                items_list[i["name"]] = new_item
                if npc == "apple" or npc == "pear":
                    heal_list[i["name"]] = new_item


def load_json():
    load_enms()
    load_locs()
    load_npcs()


def connect_locs():
    for loc in locs_list:
        locs_list.get(loc).opts["prison"] = "prison"


def print_intro():
    for i in range(1, 10):
        if i == 1:
            print(repr_mess(i, "r").format(me.name))
        else:
            repr_mess(i, "p")


def choose_difficulty(Me):
    me.diff = input(
        "\n Enter a number a number (1 - 3) to choose difficulty:\n1. Easy\n2. Medium\n3. Hard\n>")
    if me.diff == "1":
        me.inv["gold coin"] += 10
        me.inv["pear"] += 2
        repr_mess(34, "p")
    elif me.diff == "2":
        me.inv["gold coin"] += 5
        me.inv["pear"] += 1
        repr_mess(35, "p")
    elif me.diff == "3":
        repr_mess(36, "p")
    else:
        choose_difficulty(Me)


def alchem_trade(npc):
    safe = 1
    for item in npc.inv:
        if item == "Shard of Alberimus":
            pass
        elif me.inv[item] > 0 and not npc.inv[item] == items_list[item].alchem_limit:
            if me.inv[item] <= items_list[item].alchem_limit:
                x = me.inv[item] - npc.inv[item]
            else:
                x = items_list[item].alchem_limit - npc.inv[item]
            npc.inv[item] += x
            me.inv[item] -= x
            if not x == 0:
                print(repr_mess(42, "r").format(
                    x, items_list[item].name))
            elif me.inv[item] == 0 and safe == 1:
                print("You have nothing to give")
                safe += 1


def trade(npc):
    if me.loc == "alchemist2":
        alchem_trade(npc)
        if npc.inv["wolf pelt"] == items_list["wolf pelt"].alchem_limit and npc.inv["worm fang"] == items_list["worm fang"].alchem_limit and npc.inv["snake tongue"] == items_list["snake tongue"].alchem_limit and npc.inv["spider web"] == items_list["spider web"].alchem_limit:
            me.inv["Shard of Alberimus"] += npc.inv["Shard of Alberimus"]
            npc.inv["Shard of Alberimus"] -= npc.inv["Shard of Alberimus"]
            repr_mess(43, "p")
            npc.talked_to2 = True
            connect_locs()
    else:
        buy_or_sell()
        me.buy_sell()


def talked_to():
    repr_loc("mess", me.loc, "p")
    if me.loc == "alchemtalk4":
        npcs_for_loc["alchemist"].talked_to1 = True
    elif me.loc == "prisontalk":
        npcs_for_loc["prison"].talked_to1 = True


def talk_trade():
    if me.loc == "alchemist2":
        trade(npcs_for_loc["alchemist"])
    else:
        trade(npcs_for_loc[me.loc])
    me.loc = me.last_loc
    me.talking = False


def talk():
    me_opts = repr_loc(me.loc, "opts", "r")
    talked_to()
    inpt = input(">")
    if me_opts.get(inpt) == "village" or me_opts.get(inpt) == "prison":
        me.loc = me.last_loc
        me.talking = False
    elif me_opts.get(inpt) == "trade":
        talk_trade()
    elif inpt in me_opts:
        me.loc = me_opts.get(inpt)
    else:
        repr_mess(23, "p")
        talk()


def fight(enemy):
    while me.n > 0:
        if not me.on_turn:
            me.max_take = 3
            me.max_take = min(me.n, me.max_take)
            me.n -= enemy.take()
            print(repr_mess(31, "r").format(me.n))
            me.on_turn = True
        else:
            if me.inv.get("Zandalar's staff") > 0:
                me.max_take = 4
            else:
                me.max_take = 3
            me.max_take = min(me.n, me.max_take)
            me.take()
            me.on_turn = False


def fight_input(enemy, me):
    print(repr_mess(26, "r").format(me.name, enemy.name))
    fight(enemy)
    if me.n == 0:
        if me.on_turn == False:
            repr_mess(32, "p")
            enemy.trophy()
        else:
            print(repr_mess(33, "r").format(enemy.harm))
            me.health -= enemy.harm
        me.n = 21
        me.on_turn = False


def loc_check():
    tlk = ["market", "chief", "alchemist",
           "alchemist2", "alchemist3", "prisontalk"]
    if me.loc in tlk:
        me.talking = True
        while me.talking:
            talk()
    elif me.loc in hostile_locs:
        ran = random.randint(1, 100)
        if ran < hostile_locs[me.loc].chance:
            fight_input(hostile_locs[me.loc], me)


def user_input(Me, locs_list):
    loc_check()
    repr_loc("mess", me.loc, "p")
    x = input("> ")
    commands = {"chooseloc": me.choose_loc, "wait": me.wait, "avalocs": me.print_ava_locs, "combat": me.print_combat,
                "i": me.print_inv, "health": me.print_health, "heal": me.heal, "exit": me.exit, "h": me.print_hint}
    if x in commands:
        commands[x]()
    else:
        repr_mess(47, "p")


def main(Me, locs_list):
    load_json()
    me.name = input("\nChoose your name:\n>")
    choose_difficulty(Me)
    print_intro()
    while me.run:
        if me.health <= 0:
            repr_mess(38, "p")
            me.run = False
        user_input(Me, locs_list)
    if not me.run:
        repr_mess(39, "p")


hostile_locs = {}
npcs_for_loc = {}
locs_list = {}
items_list = {}
heal_list = {}

me = Me(return_char("me", "max_health"), return_char("me", "health"), return_char("me", "loc"), return_char("me", "diff"), return_char("me", "run"), return_char("me", "on_turn"), return_char("me", "n"),
        return_char("me", "min_take"), return_char("me", "max_take"), return_char("me", "talking"), return_char("me", "last_loc"), return_char("me", "inv"), return_char("me", "way"), return_char("me", "name"))

main(Me, locs_list)
