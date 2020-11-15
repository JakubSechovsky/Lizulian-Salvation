import linecache as line
import ast
import random
import json
        
class Location:
    def __init__(self, counter, place, opts):
        self.counter = counter
        self.place = place
        self.opts = opts

class NPC:
    def __init__(self, loc, inv, talked_to1, talked_to2):
        self.loc = loc
        self.inv = inv
        self.talked_to1 = talked_to1
        self.talked_to2 = talked_to2

    def trade(self):
        if me.loc == "alchemist2":
            for item in self.inv:
                if item == "Shard of Alberimus":
                    pass
                elif me.inv[item] > 0 and not self.inv[item] == items_list[item].alchem_limit:
                    if me.inv[item] <= items_list[item].alchem_limit:
                        x = me.inv[item] - self.inv[item]
                    else:
                        x = items_list[item].alchem_limit - self.inv[item]
                    self.inv[item] += x
                    me.inv[item] -= x
                    if not x == 0:
                        print(repr_mess(47, "r").format(x, items_list[item].name))
            if self.inv["wolf pelt"] == items_list["wolf pelt"].alchem_limit and self.inv["worm fang"] == items_list["worm fang"].alchem_limit and self.inv["snake tongue"] == items_list["snake tongue"].alchem_limit and self.inv["spider web"] == items_list["spider web"].alchem_limit:
                me.inv["Shard of Alberimus"] += self.inv["Shard of Alberimus"]
                self.inv["Shard of Alberimus"] -= self.inv["Shard of Alberimus"]
                repr_mess(48, "p")
                self.talked_to2 = True
                load_void()
        elif me.loc == "market":
            pass
        elif me.loc == "shrines of lizul":
            pass

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
            else:
                pass
            print(repr_mess(15, "r").format(self.healval, me.health))
        else:
            repr_mess(16, "p")

class Me:
    def __init__(self, max_health, health, level, loc, diff, run, fighting, n, min_take, max_take, talking, last_loc, inv):
        self.health = health
        self.loc = loc
        self.run = run
        self.fighting = fighting
        self.max_health = max_health
        self.diff = diff
        self.n = n
        self.max_take = max_take
        self.min_take = min_take
        self.talking = talking
        self.last_loc = last_loc
        self.inv = inv

    def print_inv(self):
        inventory = []
        for g in me.inv:
            if me.inv.get(g):
                inventory.append(g)
            else:
                pass
        repr_mess(19, "p")
        for g in inventory:
            print(repr_mess(18, "r").format(me.inv.get(g), g))
        inventory = []

    def print_health(self):
        print(repr_mess(20, "r").format(me.health))

    def print_loc(self):
        print(repr_mess(22, "r").format(me.loc))

    def heal(self):
        if me.health < me.max_health:
            y = input("Type the exact name of the item you want to use for healing:\n>")
            if y in me.inv:
                if y == "apple":
                    items_list["apple"].heal_user()
                elif y == "pear":
                    items_list["pear"].heal_user()
            else:
                print(repr_mess(23, "r").format(items_list["apple"].name, items_list["pear"].name))
        else:
            repr_mess(24, "p")

    def print_combat(self):
        for i in range(10, 14):
            repr_mess(i, "p")

    def print_ava_locs(self):
        repr_mess(27, "p")
        for i in locs_list[me.loc].opts:
            print(i)

    def print_hint(self):
        repr_mess(25, "p")

    def exit(self):
        me.run = False

    def choose_loc(self, locs):
        y = input("Type in the exact name of the location you want to go to: \n>")
        if y in locs_list[me.loc].opts:
            if y in locs:
                if y == "alchemist" and npcs_for_loc["alchemist"].talked_to2:
                    me.last_loc = me.loc
                    me.loc = "alchemist3"
                elif y == "alchemist" and npcs_for_loc["alchemist"].talked_to1:
                    me.last_loc = me.loc
                    me.loc = "alchemist2"
                else:
                    me.last_loc = me.loc
                    locs.get(y).counter = 1
                    me.loc = locs.get(me.loc).opts.get(y)
            else:
                repr_mess(25, "p")
                self.choose_loc(locs)
        else:
            repr_mess(27, "p")
            for i in locs_list[me.loc].opts:
                print(i)

    def rem_st(self, x):
        me.n -= x
        print(repr_mess(29, "r").format(x))

    def take(self):
        y = input("How many stones do you want to remove?\n>")
        st = {"1":me.rem_st, "2":me.rem_st, "3":me.rem_st}
        if y in st:
            st[y](int(y))
        else:
            repr_mess(42, "p")
            me.take()

    def talk(self):
        me_opts = repr_loc(me.loc, "opts", "r")
        repr_loc("mess", me.loc, "p")
        if me.loc == "alchemtalk4":
            npcs_for_loc["alchemist"].talked_to1 = True
        inpt = input(">")
        if me_opts.get(inpt) == "village":
            me.loc = me.last_loc
            me.talking = False
        elif me_opts.get(inpt) == "trade":
            if me.loc == "alchemist2":
                npcs_for_loc["alchemist"].trade()
            elif me.loc == "shrines of lizul":
                npcs_for_loc[me.loc].trade()
            else:
                npcs_for_loc["market"].trade()
            me.loc = me.last_loc
            me.talking = False
        elif inpt in me_opts:
            me.loc = me_opts.get(inpt)
        else:
            repr_mess(25, "p")
            self.talk()

class Enemy:
    def __init__(self, loc, loot, name, chance, harm):
        self.loot = loot
        self.loc = loc
        self.name = name
        self.chance = chance
        self.harm = harm

    def simulationAI(self):
        me.max_take = min(me.n, me.max_take)
        best_act = -1
        best_score = -float("inf")
        for x in range(me.min_take, me.max_take + 1):
            act_score = 0
            for i in range(1000):
                stone_count = me.n - x
                i_play = False
                while stone_count > 0:
                    stone_count -= min(stone_count, random.randint(me.min_take, me.max_take + 1))
                    i_play= not i_play
                if(i_play): act_score -= 1
                else: act_score += 1
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
    
    def randomAI(self):
        return random.randint(me.min_take, me.max_take)

    def trophy(self):
        ran = random.randint(1,3)
        trophy = []
        trophy.append(ran)
        trophy.append(self.loot)
        print(repr_mess(31, "r").format(trophy[0], trophy[1]))
        x = input("What do you want to do with the loot?\n1. Accept\n2.Reject\n>")
        if x == "1":
            me.inv[self.loot] += ran
            print(repr_mess(32, "r").format(trophy[0], trophy[1]))
        elif x == "2":
            print(repr_mess(33, "r").format(trophy[0], trophy[1]))
        else:
            repr_mess(34, "p")
            self.trophy()
        trophy.clear()

    def take(self):
        if self.name == "Lizul":
            x = self.perfectAI()
        elif me.diff == "1":
            x = self.randomAI()
        elif me.diff == "2":
            x = self.simulationAI()
        elif me.diff == "3" and not me.inv.get("per ardua") > 0:
            x = self.simulationAI()
        else:
            x = self.perfectAI()
        print(repr_mess(45, "r").format(self.name, x))
        return x

def repr_mess(x, way):
    with open(r"C:\Users\Jakub\Desktop\Lizulian Salvation\mess.json") as mess_file:
        mess = json.load(mess_file)
        if way == "p":
            print(mess[str(x)])
        else:
            return mess[str(x)]

def repr_loc(name, key, way):
    with open(r"C:\Users\Jakub\Desktop\Lizulian Salvation\locs.json") as locs_file:
        locs = json.load(locs_file)
        if way == "p":
            print(locs[name][key])
        else:
            return locs[name][key]

def return_char(name, key):
    with open(r"C:\Users\Jakub\Desktop\Lizulian Salvation\characters.json") as chars_file:
        chars = json.load(chars_file)
        return chars[name][key]

def load_json():
    with open(r"C:\Users\Jakub\Desktop\Lizulian Salvation\enms.json") as enms_file:
        enms = json.load(enms_file)
        for enm in enms:
            atts = enms[enm]
            new_enm = Enemy(atts["loc"], atts["loot"], atts["name"], atts["chance"], atts["harm"])
            hostile_locs[atts["loc"]] = new_enm
    with open(r"C:\Users\Jakub\Desktop\Lizulian Salvation\locs.json") as locs_file:
        locations = json.load(locs_file)
        for loc in locations:
            if loc == "mess":
                pass
            else:
                inf = locations[loc]
                new_loc = Location(inf["counter"], inf["place"], inf["opts"])
                locs_list[inf["place"]] = new_loc
    with open(r"C:\Users\Jakub\Desktop\Lizulian Salvation\characters.json") as npcs_file:
        npcs = json.load(npcs_file)
        for npc in npcs:
            if npc == "me":
                pass
            elif npc == "alchemist" or npc == "Alberimus":
                quals = npcs[npc]
                new_npc = NPC(quals["loc"], quals["inv"], quals["talked_to1"], quals["talked_to2"])
                npcs_for_loc[quals["loc"]] = new_npc
            else:
                i = npcs[npc]
                new_item = Items(i["sellval"], i["healval"], i["name"], i["alchem_limit"])
                items_list[i["name"]] = new_item

def load_void():
    void_locs = ["shrines", "talematros"]
    for loc in locs_list:
        if loc in void_locs:
            pass
        else:
            for i in range(0,6):
                locs_list[loc].opts[void_locs[i]] = void_locs[i]

def print_intro(username):
    for i in range(1, 10):
        if i == 1:
            print(repr_mess(i, "r").format(username))
        else:
            repr_mess(i, "p")

def choose_difficulty(Me):
    me.diff = input("\n Choose your difficulty by typing in a number (1 - 3):\n1. Easy\n2. Medium\n3. Hard\n>")
    if me.diff == "1":
        me.inv["gold coin"] += 10
        me.inv["pear"] += 2
        repr_mess(39, "p")
        me.run = True
    elif me.diff == "2":
        me.inv["gold coin"] += 5
        me.inv["pear"] += 1
        repr_mess(40, "p")
        me.run = True
    elif me.diff == "3":
        repr_mess(41, "p")
        me.run = True
    else:
        choose_difficulty(Me)

def fight_input(enemy, me, username):
    me.fighting = True
    print(repr_mess(30, "r").format(username, enemy.name))
    on_turn = 1
    while me.n > 0:
        if on_turn == 1:
            me.n -= enemy.take()
            print(repr_mess(35, "r").format(me.n))
            on_turn += 1
        else:
            me.take()
            on_turn = 1
    if me.n == 0:
        if on_turn == 1:
            repr_mess(36, "p")
            enemy.trophy()
        else:
            print(repr_mess(37, "r").format(enemy.harm))
            me.health -= enemy.harm
        me.fighting = False
        me.n = 21

def user_input(Me, locs_list, username):
    tlk = ["market", "chiefhut", "alchemist", "alchemist2", "alchemist3"]
    if me.loc in tlk:
        me.talking = True
        while me.talking:
            me.talk()
        repr_loc("mess", me.loc, "p")
    elif locs_list.get(me.loc).counter == 1:
        repr_loc("mess", me.loc, "p")
        locs_list.get(me.loc).counter += 1
    elif me.loc in hostile_locs:
        ran = random.randint(1, 100)
        if ran < hostile_locs[me.loc].chance:
                fight_input(hostile_locs[me.loc], me, username)
    x = input("> ")
    keys = {"avalocs":me.print_ava_locs, "combat":me.print_combat, "i":me.print_inv, "health":me.print_health, "heal":me.heal, "exit":me.exit, "h":me.print_hint}
    if x in keys and not me.fighting and not me.talking:
        keys[x]()
    elif x == "chooseloc":
        me.choose_loc(locs_list)
    else:
        repr_mess(46, "p")

def main(Me, locs_list):
    load_json()
    username = input("\nChoose your name:\n>")
    choose_difficulty(Me)
    print_intro(username)
    while me.run:
        if me.health <= 0:
            repr_mess(43, "p")
            me.run = False
        user_input(Me, locs_list, username)
    if not me.run:
        repr_mess(44, "p")

me = Me(return_char("me", "max_health"), return_char("me", "health"), return_char("me", "level"), return_char("me", "loc"), return_char("me", "diff"), return_char("me", "run"), return_char("me", "fighting"), return_char("me", "n"), return_char("me", "min_take"), return_char("me", "max_take"), return_char("me", "talking"), return_char("me", "last_loc"), return_char("me", "inventory"))

hostile_locs = {"lake":[], "forest":[], "fields":[], "mine":[]}
locs_list = {"house":[], "village":[], "lake":[], "forest":[], "fields":[], "mine":[], "market":[], "alchemist":[], "chiefhut":[], "shrines":[], "talematros":[]}
items_list = {"apple":[], "pear":[], "wolf pelt":[], "worm fang":[], "snake tongue":[], "spider web":[], "Shard of Alberimus":[], "Zandalar's staff":[]}
npcs_for_loc = {"market":[], "alchemist":[]}

main(Me, locs_list)