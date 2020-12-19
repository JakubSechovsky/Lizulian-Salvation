import random
import json
import classes as cs


def buy_or_sell():
    x = input(repr_mess(48, "r"))
    if x == "1":
        me.way = "buy"
    elif x == "2":
        me.way = "sell"
    else:
        repr_mess(41, "p")
        buy_or_sell()


def cont_trading():
    x = input(
        repr_mess(49, "r"))
    if x == "1":
        trade(npcs_for_loc[me.loc])
    elif x == "2":
        me.loc = "village"
        me.talking = False
    else:
        repr_mess(5, "p")
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
            new_enm = cs.Enemy(atts["loc"], atts["loot"], atts["name"],
                               atts["chance"], atts["harm"], atts["low_limit"], atts["up_limit"])
            hostile_locs[atts["loc"]] = new_enm


def load_locs():
    with open("./locs.json", "r", encoding="utf-8") as locs_file:
        locations = json.load(locs_file)
        for loc in locations:
            if not loc == "mess":
                inf = locations[loc]
                new_loc = cs.Location(inf["place"], inf["opts"])
                locs_list[inf["place"]] = new_loc


def load_npcs():
    with open("./characters.json", "r", encoding="utf-8") as npcs_file:
        npcs = json.load(npcs_file)
        for npc in npcs:
            i = npcs[npc]
            if not npc == "me":
                if npc == "alchemist" or npc == "merchant" or npc == "Alberimus":
                    new_npc = cs.NPC(i["loc"], i["inv"],
                                     i["talked_to1"], i["talked_to2"])
                    npcs_for_loc[i["loc"]] = new_npc
                else:
                    new_item = cs.Items(i["sellval"], i["healval"],
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


def print_intro(): print(repr_mess(1, "r").format(me.name))


def choose_difficulty(Me):
    me.diff = input(
        repr_mess(50, "r"))
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
                repr_mess(51, "p")
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
            me.min_take = 1
            me.max_take = min(me.n, 3)
            me.n -= enemy.take()
            print(repr_mess(31, "r").format(me.n))
            me.on_turn = True
        else:
            if me.inv.get("Zandalar's staff") > 0:
                me.max_take = 4
                me.min_take = 0
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
    me.name = input(repr_mess(52, "r"))
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

me = cs.Me(return_char("me", "max_health"), return_char("me", "health"), return_char("me", "loc"), return_char("me", "diff"), return_char("me", "run"), return_char("me", "on_turn"), return_char("me", "n"),
        return_char("me", "min_take"), return_char("me", "max_take"), return_char("me", "talking"), return_char("me", "last_loc"), return_char("me", "inv"), return_char("me", "way"), return_char("me", "name"))


main(cs.Me, locs_list)
