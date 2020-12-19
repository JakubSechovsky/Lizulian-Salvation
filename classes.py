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

    def heal(self):
        if self.health < self.max_health:
            y = input(
                repr_mess(3, "r"))
            if y in self.inv and y in heal_list:
                heal_list[y].heal_user()
            else:
                print(repr_mess(21, "r").format(
                    items_list["apple"].name, items_list["pear"].name))
        else:
            repr_mess(22, "p")

    def print_combat(self): repr_mess(2, "p")

    def print_ava_locs(self):
        repr_mess(24, "p")
        for i in locs_list[self.loc].opts:
            print(i)

    def print_hint(self): repr_mess(46, "p")

    def exit(self): self.run = False

    def wait(self):
        if me.loc in hostile_locs:
            fight_input(hostile_locs[me.loc], me)

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
        y = input(repr_mess(6, "r"))
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
        y = input(repr_mess(4, "r"))
        try:
            y = int(y)
            if y in range(me.min_take, me.max_take + 1):
                me.rem_st(y)
            else:
                print(repr_mess(37, "r").format(
                    me.max_take, me.min_take))
                self.take()
        except ValueError:
            repr_mess(5, "p")
            self.take()

    def buy(self, x):
        y = input(repr_mess(7, "r").format(
            x, self.way, items_list[x].buyval))
        try:
            y = int(y)
            z = y*items_list[x].buyval
            if z > self.inv.get("gold coin"):
                print(repr_mess(8, "r").format(x))
            else:
                self.inv["gold coin"] -= z
                self.inv[x] += y
                print(repr_mess(9, "r").format(y, x, z))
        except ValueError:
            repr_mess(5, "p")
            self.buy(x)

    def sell(self, x):
        y = input(repr_mess(10, "r").format(
            self.inv.get(x), x, items_list[x].sellval))
        try:
            y = int(y)
            if y > self.inv.get(x) or y < 0:
                repr_mess(5, "p")
                self.sell(x)
            else:
                z = y*items_list[x].sellval
                self.inv["gold coin"] += z
                self.inv[x] -= y
                print(repr_mess(11, "r").format(z, y, x))
        except ValueError:
            repr_mess(5, "p")
            self.sell(x)

    def buy_sell(self):
        x = input(repr_mess(12, "r").format(self.way))
        if x in self.inv:
            if x == "Shard of Alberimus" or x == "Zandalar's staff":
                print(repr_mess(13, "r").format(self.way))
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

    def randomAI(self): return random.randint(
        me.min_take, me.max_take)

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
                repr_mess(14, "r"))
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
