from json import load


class Location:
    def __init__(self, place, opts):
        self.place = place
        self.opts = opts


class NPC:
    def __init__(self, atts):
        for key in atts:
            setattr(self, key, atts[key])


class Items:
    def __init__(self, atts):
        for key in atts:
            setattr(self, key, atts[key])

        self.buyval = 2 * self.sellval

    def heal_user(self):
        """
        Kontroluje, zda hráč vybraný předmět vlastní
        Pokud ano, hráče vyléčí
        """
        if me.inv.get(self.name) > 0:
            me.health += self.healval
            me.inv[self.name] -= 1

            if me.health > me.max_health:
                me.health = me.max_health

            message = repr_mess("heal_succ", "r", mess)
            print(message.format(self.healval, me.health))
        else:
            repr_mess("no_item", "p", mess)


class Me:
    def __init__(self, atts):
        for key in atts:
            setattr(self, key, atts[key])

    def print_inv(self):
        """
        Vypisuje seznam předmětů v hráčově inventáři spolu s jejich počtem
        """
        repr_mess("print_inv", "p", mess)
        message = repr_mess("inv_items", "r", mess)

        for item in self.inv:
            if self.inv.get(item) > 0:
                print(message.format(self.inv.get(item), item))

    def print_health(self):
        """
        Vypisuje aktuální počet hráčových životů
        """
        print(repr_mess("health", "r", mess).format(self.health))

    def heal(self):
        """
        Kontroluje hráčovy životy, případně iniciuje léčení hráče
        """
        if self.health < self.max_health:
            heal_item = input(repr_mess("heal_item", "r", mess))

            if heal_item in self.inv and heal_item in heal_list:
                heal_list[heal_item].heal_user()
            else:
                print(
                    repr_mess("heal_opts", "r", mess).format(
                        items_list["apple"].name, items_list["pear"].name
                    )
                )
        else:
            repr_mess("full_health", "p", mess)

    def print_combat(self):
        """
        Vypisuje zprávu o soubojovém systému
        """
        repr_mess("combat", "p", mess)

    def print_intro(self):
        """
        Vypisuje úvod do hry
        """
        print(repr_mess("intro", "r", mess).format(self.name))

    def print_ava_locs(self):
        """
        Vypisuje seznam lokací, do kterých hráč ze své aktuální lokace může
        """
        repr_mess("loc_opts", "p", mess)

        for option in locs_list[self.loc].opts:
            print(option)

    def print_hint(self):
        """
        Vypisuje všechny možné příkazy ve hře
        """
        repr_mess("hint", "p", mess)

    def exit(self):
        """
        Ukončuje hru
        """
        self.run = False

    def choose_loc(self):
        """
        Ptá se hráče, do které lokace se chce přesunout a jedná podle vstupu
        """
        inpt_loc = input(repr_mess("loc", "r", mess))

        if inpt_loc == self.loc:
            repr_mess("in_loc", "p", mess)
        else:
            if inpt_loc in locs_list[self.loc].opts:
                self.choose_loc_check(inpt_loc)
            else:
                repr_mess("invalid_loc", "p", mess)

                for loc in locs_list[self.loc].opts:
                    print(loc)

    def choose_loc_check(self, inpt_loc):
        """
        Podle booleanů, které určují, jaké rozohovory hráč již vedl
        """
        tlk1 = inpt_loc == "alchemist" and npcs_for_loc["alchemist"].talked_to2
        tlk2 = inpt_loc == "alchemist" and npcs_for_loc["alchemist"].talked_to1
        tlk3 = (
            self.loc == "prison"
            and not inpt_loc == "village"
            and not npcs_for_loc["prison"].talked_to1
        )
        tlk4 = inpt_loc == "altar" and npcs_for_loc["altar"].talked_to1
        self.last_loc = self.loc

        self.choose_loc_assign(inpt_loc, tlk1, tlk2, tlk3, tlk4)

    def choose_loc_assign(self, inpt_loc, tlk1, tlk2, tlk3, tlk4):
        """
        Přiřazuje hráči lokaci podle booleanů
        """
        if tlk1:
            self.loc = "alchemist3"
        elif tlk2:
            self.loc = "alchemist2"
        elif tlk3:
            self.loc = "alb"
        elif tlk4:
            self.loc = "altar2"
        else:
            self.loc = locs_list.get(self.loc).opts.get(inpt_loc)

    def take(self):
        """
        Ptá se hráče na počet kamenů, které chce odebrat
        Jedná podle vstupu
        """
        take_num = input(repr_mess("stone_number", "r", mess))
        try:
            take_num = int(take_num)

            if take_num in range(self.min_take, self.max_take + 1):
                self.n -= take_num
                print(repr_mess("stones_removed", "r", mess).format(take_num))
            else:
                message = repr_mess("stone_limit", "r", mess)
                print(message.format(self.max_take, self.min_take))
                self.take()
        except ValueError:
            repr_mess("int_error", "p", mess)
            self.take()

    def buy(self, item):
        """
        Ptá se hráče na počet předmětů, které chce nakoupit
        Pokud je to možné, provede jejich nákup
        """
        amount = input(
            repr_mess("buy", "r", mess).format(
                item, items_list[item].buyval, self.inv.get("gold coin"), mess
            )
        )
        try:
            amount = int(amount)
            cost = amount * items_list[item].buyval

            if cost > self.inv.get("gold coin"):
                print(repr_mess("need_gold", "r", mess).format(item))
            else:
                self.inv["gold coin"] -= cost
                self.inv[item] += amount
                message = repr_mess("buy_succ", "r", mess)
                print(message.format(amount, item, cost))
        except ValueError:
            repr_mess("int_error", "p", mess)
            self.buy(item)

    def sell(self, item):
        """
        Ptá se hráče na počet předmětů, které chce prodat
        Pokud je to možné, provede jejich prodej
        """
        amount = input(
            repr_mess("sell", "r", mess).format(
                self.inv.get(item),
                item,
                items_list[item].sellval,
                self.inv.get("gold coin"),
            )
        )
        try:
            amount = int(amount)

            if amount > self.inv.get(item) or amount < 0:
                print(repr_mess("no_items", "r", mess).format(item))
                self.sell(item)
            else:
                cost = amount * items_list[item].sellval
                message = repr_mess("sell_succ", "r", mess)
                self.inv["gold coin"] += cost
                self.inv[item] -= amount
                print(message.format(cost, amount, item))
        except ValueError:
            repr_mess("int_error", "p", mess)
            self.sell(item)

    def choose_difficulty(self):
        """
        Zprostředkovává výběr obtížnosti
        """
        self.diff = input(repr_mess("choose_diff", "r", mess))

        if self.diff == "1":
            self.inv["gold coin"] += 10
            self.inv["apple"] += 1
            repr_mess("easy", "p", mess)
        elif self.diff == "2":
            repr_mess("hard", "p", mess)
        else:
            try_int(self.diff)
            self.choose_difficulty()


def repr_mess(x, way, mess):
    """
    Vypíše, případně vrátí zprávu ze slovníku mess
    """
    if way == "p":
        print(mess[x])
    else:
        return mess[x]


def repr_loc(name, key, way, locs):
    """
    Vypíše, případně vrátí informaci / zprávu ze slovníku locs
    """
    if way == "p":
        print(locs[name][key])
    else:
        return locs[name][key]


def connect_locs():
    """
    'Spojuje' lokace, čímž umožňuje hráči průchod mezi nimi
    """
    locs_list.get("village").opts["prison"] = "prison"


def load_locs():
    """
    Načítá data o lokacích ze souboru locs.json
    """
    with open("./locs.json", "r", encoding="utf-8") as locs_file:
        locations = load(locs_file)

        for loc in locations:
            if not loc == "mess":
                info = locations[loc]
                new_loc = Location(info["place"], info["opts"])
                locs_list[info["place"]] = new_loc


def load_npcs():
    """
    Načítá data o předmětech a postavách ze souboru characters.json
    """
    with open("./characters.json", "r", encoding="utf-8") as npcs_file:
        npcs = load(npcs_file)

        for npc in npcs:
            npc_check(npcs, npc)


def npc_check(npcs, npc):
    """
    Ukládá načtená data jako instance třídy,
    které následné uloží do příslušného seznamu
    """
    atts = npcs[npc]
    npcs = ["alchemist", "merchant", "Alberimus", "altar"]

    if npc == "me":
        new_player = Me(atts)
        me["diff"] = new_player
    else:
        if npc in npcs:
            new_npc = NPC(atts)
            npcs_for_loc[atts["loc"]] = new_npc
        else:
            new_item = Items(atts)
            items_list[atts["name"]] = new_item

            if npc == "apple" or npc == "pear":
                heal_list[atts["name"]] = new_item


def try_int(user_input):
    """
    Testuje, zda uživatel zadal platný vstup
    """
    try:
        int(user_input)
        repr_mess("invalid_opt", "p", mess)
    except ValueError:
        repr_mess("int_error", "p", mess)


with open("./mess.json", "r", encoding="utf-8") as mess_file:
    mess = load(mess_file)

with open("./locs.json", "r", encoding="utf-8") as locs_file:
    locs = load(locs_file)

# seznamy, do kterých se ukládají instance jednotlivých tříd
hostile_locs = {}
npcs_for_loc = {}
locs_list = {}
items_list = {}
heal_list = {}
me = {}
