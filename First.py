import random
import json
import Second as sec


class Enemy:
    def __init__(self, loc, loot, name, chance, harm, low_limit, up_limit, best_act):
        self.loot = loot
        self.loc = loc
        self.name = name
        self.chance = chance
        self.harm = harm
        self.low_limit = low_limit
        self.up_limit = up_limit
        self.best_act = best_act

    def simulationAI(self):
        self.best_act = -1
        best_score = -float("inf")
        for x in range(me.min_take, me.max_take + 1):
            act_score = 0
            self.simulationAI2(x, best_score, act_score)
        return self.best_act

    def simulationAI2(self, x, best_score, act_score):
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
            self.best_act = x

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

    def randomAI(self): return random.randint(
        me.min_take, me.max_take)

    def trophy(self):
        ran = random.randint(self.low_limit, self.up_limit)
        if ran == 0:
            sec.repr_mess("no_offer", "p")
        else:
            self.trophy2(ran)

    def trophy2(self, ran):
        print(sec.repr_mess("offer", "r").format(ran, self.loot))
        x = input(
            sec.repr_mess("loot", "r"))
        if x == "1":
            me.inv[self.loot] += ran
            print(sec.repr_mess("received", "r").format(
                ran, self.loot))
        elif x == "2":
            print(sec.repr_mess("rejected", "r").format(
                ran, self.loot))
        else:
            sec.repr_mess("int_error", "p")
            self.trophy()

    def take(self):
        if not me.inv.get("Zandalar's staff") > 0:
            ai = {"1": self.randomAI, "2": self.simulationAI,
                  "3": self.simulationAI}
            x = ai[me.diff]()
        else:
            x = self.perfectAI()
        print(sec.repr_mess("enemy_take", "r").format(self.name, x))
        return x


def wait():
    if me.loc in sec.hostile_locs:
        fight_input(sec.hostile_locs[me.loc], me)


def buy_sell():
    x = input(sec.repr_mess("market_item", "r").format(me.way))
    if x in me.inv:
        if x == "Shard of Alberimus" or x == "Zandalar's staff":
            print(sec.repr_mess("no_market", "r").format(me.way))
        else:
            if me.way == "buy":
                me.buy(x)
            elif me.way == "sell" and me.inv.get(x) > 0:
                me.sell(x)
    else:
        sec.repr_mess("no_item", "p")
    cont_trading()


def buy_or_sell():
    x = input(sec.repr_mess("buy_or_sell", "r"))
    if x == "1":
        me.way = "buy"
    elif x == "2":
        me.way = "sell"
    else:
        sec.repr_mess("int_error", "p")
        buy_or_sell()
    buy_sell()


def cont_trading():
    x = input(
        sec.repr_mess("cont_trade", "r"))
    if x == "1":
        trade(sec.npcs_for_loc[me.loc])
    elif x == "2":
        me.loc = "village"
        me.talking = False
    else:
        sec.repr_mess("int_error", "p")
        cont_trading()


def load_enms():
    with open("./enms.json", "r", encoding="utf-8") as enms_file:
        enms = json.load(enms_file)
        for enm in enms:
            atts = enms[enm]
            new_enm = Enemy(atts["loc"], atts["loot"], atts["name"],
                            atts["chance"], atts["harm"], atts["low_limit"], atts["up_limit"], atts["best_act"])
            sec.hostile_locs[atts["loc"]] = new_enm


def load_json():
    load_enms()
    sec.load_locs()
    sec.load_npcs()


def alchem_trade(npc):
    me.safe = 1
    for item in npc.inv:
        if not item == "Shard of Alberimus":
            if me.inv[item] > 0 and not npc.inv[item] == sec.items_list[item].alchem_limit:
                alchem_trade2(npc, item)
            elif me.inv[item] == 0 and me.safe == 1:
                sec.repr_mess("give_nothing", "p")
                me.safe += 1


def alchem_trade2(npc, item):
    if me.inv[item] <= sec.items_list[item].alchem_limit:
        x = me.inv[item] - npc.inv[item]
    else:
        x = sec.items_list[item].alchem_limit - npc.inv[item]
    npc.inv[item] += x
    me.inv[item] -= x
    if not x == 0:
        print(sec.repr_mess("alchem_give", "r").format(
            x, sec.items_list[item].name))
    elif me.inv[item] == 0 and me.safe == 1:
        sec.repr_mess("give_nothing", "p")
        me.safe += 1


def trade(npc):
    if me.loc == "alchemist2":
        alchem_trade(npc)
        if npc.inv["wolf pelt"] == sec.items_list["wolf pelt"].alchem_limit and npc.inv["worm fang"] == sec.items_list["worm fang"].alchem_limit and npc.inv["snake tongue"] == sec.items_list["snake tongue"].alchem_limit and npc.inv["spider web"] == sec.items_list["spider web"].alchem_limit:
            me.inv["Shard of Alberimus"] += npc.inv["Shard of Alberimus"]
            npc.inv["Shard of Alberimus"] -= npc.inv["Shard of Alberimus"]
            sec.repr_mess("alchem_shard", "p")
            npc.talked_to2 = True
            sec.connect_locs()
    else:
        buy_or_sell()


def talked_to():
    sec.repr_loc("mess", me.loc, "p")
    if me.loc == "alchemtalk4":
        sec.npcs_for_loc["alchemist"].talked_to1 = True
    elif me.loc == "prisontalk":
        sec.npcs_for_loc["prison"].talked_to1 = True


def talk_trade():
    if me.loc == "alchemist2":
        trade(sec.npcs_for_loc["alchemist"])
    else:
        trade(sec.npcs_for_loc[me.loc])
    me.loc = me.last_loc
    me.talking = False


def talk():
    me_opts = sec.repr_loc(me.loc, "opts", "r")
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
        sec.repr_mess("invalid_opt", "p")
        talk()


def fight(enemy):
    while me.n > 0:
        if not me.on_turn:
            me.min_take = 1
            me.max_take = min(me.n, 3)
            me.n -= enemy.take()
            print(sec.repr_mess("stones_on_board", "r").format(me.n))
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
    print(sec.repr_mess("under_att", "r").format(me.name, enemy.name))
    fight(enemy)
    if me.n == 0:
        if me.on_turn == False:
            sec.repr_mess("fight_won", "p")
            enemy.trophy()
        else:
            print(sec.repr_mess("fight_lost", "r").format(enemy.harm))
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
    elif me.loc in sec.hostile_locs:
        ran = random.randint(1, 100)
        if ran < sec.hostile_locs[me.loc].chance:
            fight_input(sec.hostile_locs[me.loc], me)


def user_input(Me, locs_list):
    loc_check()
    sec.repr_loc("mess", me.loc, "p")
    x = input("> ")
    commands = {"chooseloc": me.choose_loc, "wait": wait, "avalocs": me.print_ava_locs, "combat": me.print_combat,
                "i": me.print_inv, "health": me.print_health, "heal": me.heal, "exit": me.exit, "h": me.print_hint}
    if x in commands:
        commands[x]()
    else:
        sec.repr_mess("invalid_comm", "p")


def main(Me, locs_list):
    load_json()
    me.name = input(sec.repr_mess("choose_name", "r"))
    me.choose_difficulty()
    me.print_intro()
    while me.run:
        if me.health <= 0:
            sec.repr_mess("dead", "p")
            me.run = False
        user_input(Me, locs_list)
    if not me.run:
        sec.repr_mess("end", "p")


me = sec.me

main(sec.Me, sec.locs_list)
