# importuje json knihovnu
from json import load


class Location:  # definuje třídu Location a její atributy
    def __init__(self, place, opts):
        self.place = place
        self.opts = opts


class NPC:  # definuje třídu NPC a její atributy
    def __init__(self, loc, inv, talked_to1, talked_to2):
        self.loc = loc
        self.inv = inv
        self.talked_to1 = talked_to1
        self.talked_to2 = talked_to2


class Items:  # definuje třídu Items a její atributy a metodu heal_user()
    def __init__(self, sellval, healval, name, alchem_limit, chapel_limit):
        self.sellval = sellval
        self.buyval = 2*sellval
        self.healval = healval
        self.name = name
        self.alchem_limit = alchem_limit
        self.chapel_limit = chapel_limit

    def heal_user(self):  # pokud má hráč v inventáři věc, se kterou se chce léčit zvýší hráčovy životy o hodnotu healval a odstraní věc z hráčova inventáře, pokud hráč věc nemá, vytiskne chybovou hlášku
        if me.inv.get(self.name) > 0:
            me.health += self.healval
            me.inv[self.name] -= 1
            # pokud jsou hráčovy životy po vyléčení větší, než maximální počet jeho životů, nastaví počet jeho životů na jejich maximální počet
            if me.health > me.max_health:
                me.health = me.max_health
            # vytiskne zprávu o kolik se zvýšily hráčovy životy a počet jeho aktuálních životů
            print(repr_mess("heal_succ", "r").format(self.healval, me.health))
        else:
            repr_mess("no_item", "p")


class Me:  # definuje třídu Me a její atributy a metody
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

    def print_inv(self):  # vytiskne seznam položek a jejich množství v aktuálním hráčově inventáři
        repr_mess("print_inv", "p")
        for g in self.inv:
            if self.inv.get(g) > 0:
                print(repr_mess("inv_items", "r").format(self.inv.get(g), g))

    # vytiskne aktuální počet hráčových životů
    def print_health(self): print(repr_mess("health", "r").format(
        self.health))

    def heal(self):  # kontroluje, zda má hráč méně životů, než je jejich maximální počet, pokud ne, vytiskne zprávu, že se nemá cenu léčit
        # pokud ano, zeptá se hráče, čím se chce vyléčit
        if self.health < self.max_health:
            y = input(
                repr_mess("heal_item", "r"))
            # pokud je vstup validní, spustí metodu heal_user() třídy Items
            if y in self.inv and y in heal_list:
                heal_list[y].heal_user()
            # pokud validní není, vypíše hráčovy možnosti
            else:
                print(repr_mess("heal_opts", "r").format(
                    items_list["apple"].name, items_list["pear"].name))
        else:
            repr_mess("full_health", "p")

    # vypíše zprávu o tom, jak funguje soubojový systém
    def print_combat(self): repr_mess("combat", "p")

    # vypíše úvod do hry
    def print_intro(self): print(repr_mess("intro", "r").format(self.name))

    def print_ava_locs(self):  # vypíše lokace, kam se hráč ze své aktuální lokace může dostat
        repr_mess("loc_opts", "p")
        for i in locs_list[self.loc].opts:
            print(i)

    # vypíše všechny možné příkazy
    def print_hint(self): repr_mess("hint", "p")

    def exit(self): self.run = False  # ukončí hru

    def choose_loc(self):  # zeptá se hráče kam chce jít
        y = input(repr_mess("loc", "r"))
        # pokud hráč už je v lokaci, kam chce jít, vytiskne o tom zprávu
        if y == self.loc:
            repr_mess("in_loc", "p")
        # pokud hráč napsal lokaci špatně / zadal něco jiného, vypíše chybovou hlášku a hráčovy možnosti, jinak zavaolá metodu choose_loc_check(y)
        else:
            if y in locs_list[self.loc].opts:
                self.choose_loc_check(y)
            else:
                repr_mess("invalid_loc", "p")
                for i in locs_list[self.loc].opts:
                    print(i)

    def choose_loc_check(self, y):
        # pokud je hráčův vstup ve slovníku možných lokací, nastaví hráčovu poslední lokaci na jeho aktuální, kterou změní na základě různých booleanů, které se mění podle toho, s kým hráč mluvil / kde byl
        if y in locs_list:
            self.last_loc = self.loc
            if y == "alchemist" and npcs_for_loc["alchemist"].talked_to2:
                self.loc = "alchemist3"
            elif y == "alchemist" and npcs_for_loc["alchemist"].talked_to1:
                self.loc = "alchemist2"
            elif self.loc == "prison" and not y == "village" and not npcs_for_loc["prison"].talked_to1:
                self.loc = "alb"
            elif y == "altar" and npcs_for_loc["altar"].talked_to1:
                self.loc = "altar2"
            # ve všech ostatních případech přesune hráče do zadané lokace
            else:
                self.loc = locs_list.get(self.loc).opts.get(y)
        # při neplatném vstupu vypíše chybovou hlášku a zavolá se rekurzivně zpátky
        else:
            repr_mess("invalid_opt", "p")
            self.choose_loc()

    def take(self):  # zeptá se hráče kolik kamenů chce odstranit
        y = input(repr_mess("stone_number", "r"))
        try:
            # pokud je vstup číslo, zkontroluje, zda je možné tento počet kamenů odebrat, pokud ano, odebere tento počet kamenů a napíše o tom zprávu
            y = int(y)
            if y in range(self.min_take, self.max_take + 1):
                self.n -= y
                print(repr_mess("stones_removed", "r").format(y))
            # pokud ne, vypíše chybovou hlášku (jaké jsou limity pro počet kamenů k odebrání) a zavolá se rekurzivně zpátky
            else:
                print(repr_mess("stone_limit", "r").format(
                    self.max_take, self.min_take))
                self.take()
        # pokud vstup není číslo, požádá hráče, aby číslo zadal a zavolá se rekurzivně zpátky
        except ValueError:
            repr_mess("int_error", "p")
            self.take()

    def buy(self, x):  # zeptá se hráče kolik věcí (y) chce koupit
        y = input(repr_mess("buy", "r").format(
            x, items_list[x].buyval, self.inv.get("gold coin")))
        try:
            # pokud hráč zadal číslo, do proměnné z načte celkovou cenu nákupu, když je z větší, než počet peněz v hráčově inventáři, vypíše chybovou hlášku
            y = int(y)
            z = y*items_list[x].buyval
            if z > self.inv.get("gold coin"):
                print(repr_mess("need_gold", "r").format(x))
            # pokud hráč má dostatek peněz na nákup, přičte se zadaný počet věcí do hráčova inventáře, odečte se jejich celková cena a vypíše se zpráva o transakci
            else:
                self.inv["gold coin"] -= z
                self.inv[x] += y
                print(repr_mess("buy_succ", "r").format(y, x, z))
        # pokud hráč nezadá číslo, poprosí hráče o zadání čísla a zavolá se rekurzivně zpátky
        except ValueError:
            repr_mess("int_error", "p")
            self.buy(x)

    def sell(self, x):  # zeptá se hráče kolik věcí (y) chce prodat
        y = input(repr_mess("sell", "r").format(
            self.inv.get(x), x, items_list[x].sellval, self.inv.get("gold coin")))
        try:
            # pokud hráč zadal číslo,kontroluje, zda je počet prodávaných věcí větší, než jejich počet v hráčově inventáři, a pokud ano, vypíše chybovou hlášku
            y = int(y)
            if y > self.inv.get(x) or y < 0:
                print(repr_mess("no_items", "r").format(x))
                self.sell(x)
            # pokud hráč zadaný počet věcí vlastní, odečte se tento počet věcí z jeho inventáře a přičte se jejich celková prodejní hodnota k hráčově počtu peněz a o transakci se vypíše zpráva
            else:
                self.inv["gold coin"] += y*items_list[x].sellval
                self.inv[x] -= y
                print(repr_mess("sell_succ", "r").format(
                    items_list[x].sellval, y, x))
        # pokud hráč nezadá číslo, poprosí hráče o zadání čísla a zavolá se rekurzivně zpátky
        except ValueError:
            repr_mess("int_error", "p")
            self.sell(x)

    # umožňuje hráči vybrat obtížnost, kterou ukládá do self.diff (me.diff) a podle výběru případně přidá věci do hráčova inventáře
    def choose_difficulty(self):
        self.diff = input(
            repr_mess("choose_diff", "r"))
        if self.diff == "1":
            self.inv["gold coin"] += 10
            self.inv["apple"] += 1
            repr_mess("easy", "p")
        elif self.diff == "2":
            self.inv["gold coin"] += 5
            self.inv["pear"] += 1
            repr_mess("medium", "p")
        elif self.diff == "3":
            repr_mess("hard", "p")
        # pokud hráč zadá jiné číslo, požádá o správný vstup a pokud hráč zadá něco jiného, než číslo, požádá ho o číslo, v obou případech se rekurzivně zavolá zpátky
        else:
            try:
                int(self.diff)
                repr_mess("invalid_opt", "p")
            except ValueError:
                repr_mess("int_error", "p")
            self.choose_difficulty()


def repr_mess(x, way):  # načítá zprávy ze souboru mess.json v závislosti na jejím kódu (x) a způsobu načtení (way), podle x najde danou zprávu a podle way ji buď vytiskne, nebo vrátí
    with open("./mess.json", "r", encoding="utf-8") as mess_file:
        mess = load(mess_file)
        if way == "p":
            print(mess[x])
        else:
            return mess[x]


def repr_loc(name, key, way):  # načítá informace o lokacích ze souboru locs.json, funguje jakožto dodatečná funkce ke třídě Location
    with open("./locs.json", "r", encoding="utf-8") as locs_file:
        # podle argumentů určuje co se bude dít - name určuje zda se otevře lokace, nebo zpráva pro lokaci, key určuje informaci pro lokaci určenou v name, případně označuje zprávu pro lokaci
        # way, stejně jako u funkce repr_mess() určuje způsob načtení - buď se informace/ zpráva vytiskne, nebo vrátí
        locs = load(locs_file)
        if way == "p":
            print(locs[name][key])
        else:
            return locs[name][key]


def return_char(key):  # načítá informace o postavě hráče podle argumentu key
    with open("./characters.json", "r", encoding="utf-8") as chars_file:
        chars = load(chars_file)
        return chars["me"][key]


def connect_locs():  # umožňoje hráči jít z lokace "village" do lokace "prison"
    locs_list.get("village").opts["prison"] = "prison"


def load_locs():  # načítá lokace ze souboru locs.json a ukládá je do slovníku locs_list jakožto instanci třídy Location pod jménem jejich místa "place"
    with open("./locs.json", "r", encoding="utf-8") as locs_file:
        locations = load(locs_file)
        for loc in locations:
            if not loc == "mess":
                inf = locations[loc]
                new_loc = Location(inf["place"], inf["opts"])
                locs_list[inf["place"]] = new_loc


def load_npcs():  # načítá vedlejší postavy a předměty
    with open("./characters.json", "r", encoding="utf-8") as npcs_file:
        npcs = load(npcs_file)
        for npc in npcs:
            npc_check(npcs, npc)


def npc_check(npcs, npc):  # ukládá postavy do slovníku npcs_for_loc, předměty do slovníku items_list a předměty, se kterými se hráč může léčit i do slovníku heal_list
    # položky ve slovnících jsou ukládány jakožto instance tříd NPC a Items (v tomto pořadí), vedlejší postavy pod názvem lokace, ve které se nacházejí a předměty pod jejich jménem
    i = npcs[npc]
    npcs = ["alchemist", "merchant", "Alberimus", "altar"]
    if not npc == "me":
        if npc in npcs:
            new_npc = NPC(i["loc"], i["inv"],
                          i["talked_to1"], i["talked_to2"])
            npcs_for_loc[i["loc"]] = new_npc
        else:
            new_item = Items(i["sellval"], i["healval"],
                             i["name"], i["alchem_limit"], i["chapel_limit"])
            items_list[i["name"]] = new_item
            if npc == "apple" or npc == "pear":
                heal_list[i["name"]] = new_item


# slovníky, do kterých se načítají data ze souborů characters.json, enms.json, locs.json a mess.json pomocí funkcí load_locs(), load_npcs() a load_enms() (v souboru First.py)
hostile_locs = {}
npcs_for_loc = {}
locs_list = {}
items_list = {}
heal_list = {}

# načtení postavy hráče jakožto instance třídy Me
me = Me(return_char("max_health"), return_char("health"), return_char("loc"), return_char("diff"), return_char("run"), return_char("on_turn"), return_char("n"),
        return_char("min_take"), return_char("max_take"), return_char("talking"), return_char("last_loc"), return_char("inv"), return_char("way"), return_char("name"), return_char("safe"))
