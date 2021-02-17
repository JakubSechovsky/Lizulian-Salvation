from random import randint
from json import load
import Second as sec


class Enemy:
    def __init__(self, atts):
        for key in atts:
            setattr(self, key, atts[key])

        self.best_score = -float("inf")

    def take(self):
        """
        Určuje počet kamenů, které hráčův oponent vezme na základě obtížnosti,
        či podle toho, zda hráč vlastní věc 'Zandalar's staff', nebo ne
        """
        if sec.me["diff"].inv.get("Zandalar's staff") > 0:
            remove_num = self.perfectAI()
        else:
            remove_num = self.perfectAI()
            ai = {"1": self.randomAI, "2": self.simulationAI}
            remove_num = ai[sec.me["diff"].diff]()

        print(sec.repr_mess("enemy_take", "r").format(self.name, remove_num))
        return remove_num

    def randomAI(self):
        """
        'Lehká obtížnost'
        Vybírá náhodné číslo z množiny možných
        """
        return randint(sec.me["diff"].min_take, sec.me["diff"].max_take)

    def simulationAI(self):
        """
        Vybírá nejlepší tah na základě simulace tahů
        """
        self.best_act = -1
        self.best_score = -float("inf")
        min_take = sec.me["diff"].min_take
        max_take = sec.me["diff"].max_take + 1

        for x in range(min_take, max_take):
            act_score = 0
            self.simulationAI2(x, act_score, min_take, max_take)
        return self.best_act

    def simulationAI2(self, x, act_score, min_take, max_take):
        """
        Provádí simulaci jako takovou
        S větší proměnnou num je simulace přesnější, ale výrazně pomalejší

        Proměnná act_score určuje,
        zda jednu danou simulaci (jednu iteraci for cyklu)
        AI vyhrála (+1), či ne (-1)

        Každá možnost AI (proměnná x) má jiné act_score,
        funkce vrátí x s největším act_score (proměnná self.best_score)
        """
        num = 1000
        for _ in range(num):
            stone_count = sec.me["diff"].n - x
            ai_turn = False

            while stone_count > 0:
                rand_num = randint(min_take, max_take)
                stone_count -= min(stone_count, rand_num)
                ai_turn = not ai_turn

            if ai_turn:
                act_score -= 1
            else:
                act_score += 1

        if act_score > self.best_score:
            self.best_score = act_score
            self.best_act = x

    def perfectAI(self):
        """
        Rozdělí všechna čísla v intervalu <0; aktuální počet kamenů>
        do setů podle toho, zda z nich hráč může vyhrát,
        nebo z nich vždy prohraje (při správných výstupech AI)

        Každou ze svých možností otestuje a vrátí tu,
        se kterou zredukuje počet kamenů na jedno z čísel v prohrávajícím setu

        Pokud se stane, že je aktuální počet kamenů v prohrávajícím setu
        a AI je na tahu, vrátí hodnotu vygenerovanou pomocí simulationAI(),
        čímž nechává hráči nejvíce místa k udělání chyby
        """
        l_nums = set([])
        w_nums = set([])
        min_take = sec.me["diff"].min_take
        max_take = sec.me["diff"].max_take + 1

        for x in range(0, sec.me["diff"].n + 1):
            for i in range(min_take, max_take):
                if x - i in l_nums:
                    w_nums.add(x)
            if x not in w_nums:
                l_nums.add(x)

        for i in range(min_take, max_take):

            if sec.me["diff"].n - i in l_nums:

                return i

        return self.simulationAI()

    def trophy(self):
        """
        Pokud hráč vyhraje nad oponentem, vybere náhodné číslo
        z intervalu čísel, která jsou daná v souboru enms.json

        Pokud je vybrané číslo 0, vypíše, že hráč nic nedostal
        """
        rand_num = randint(self.low_limit, self.up_limit)

        if rand_num == 0:
            sec.repr_mess("no_offer", "p")
        else:
            self.trophy2(rand_num)

    def trophy2(self, rand_num):
        """
        Pokud oponentovo jméno je 'Sargelaz', přidá kořist do hráčova inventáře
        V ostatních případech hráče upozorní, že má možnost kořist získat
        """
        if self.name == "Sargelaz":
            sec.repr_mess("sarg_loot", "p")
            sec.me["diff"].inv[self.loot] += rand_num
        else:
            print(sec.repr_mess("offer", "r").format(rand_num, self.loot))
            self.trophy_input(rand_num)

    def trophy_input(self, ran):
        """
        Zeptá se hráče, zda kořist chce a podle odpovědi jedná
        """
        x = input(sec.repr_mess("loot", "r"))

        if x == "1":
            sec.me["diff"].inv[self.loot] += ran
            print(sec.repr_mess("received", "r").format(ran, self.loot))
        elif x == "2":
            print(sec.repr_mess("rejected", "r").format(ran, self.loot))
        else:
            try:
                int(x)
                sec.repr_mess("invalid_opt", "p")
            except ValueError:
                sec.repr_mess("int_error", "p")
            self.trophy()


def main(Me, locs_list):
    """
    Hlavní funkce hry, volá úvodní funkce
    Kontroluje stav hráče
    """
    load_json()
    sec.me["diff"].name = input(sec.repr_mess("choose_name", "r"))
    sec.me["diff"].choose_difficulty()
    sec.me["diff"].print_intro()

    while sec.me["diff"].run:
        if sec.me["diff"].health <= 0:
            sec.repr_mess("dead", "p")
            sec.me["diff"].run = False
        if sec.me["diff"].run:
            user_input(Me, locs_list)
        else:
            sec.repr_mess("end", "p")


def load_json():
    """
    Dává dohromady funkce na načítání dat z .json souborů
    """
    load_enms()
    sec.load_locs()
    sec.load_npcs()


def load_enms():
    """
    Ze souboru enms.json načte data o potenciálních hráčových oponentech,
    které uloží jako instanci třídy a do listu,
    podle kterého jsou pak oponenti voláni
    """
    with open("./enms.json", "r", encoding="utf-8") as enms_file:
        enms = load(enms_file)
        for enm in enms:
            atts = enms[enm]
            new_enm = Enemy(atts)
            sec.hostile_locs[atts["loc"]] = new_enm


def user_input(Me, locs_list):
    """
    Umožňuje hráči vstupovat do hry a psát příkazy
    Píše zprávu, která je dána hráčovou aktuální lokací
    """
    talk_check()
    sec.repr_loc("mess", sec.me["diff"].loc, "p")
    fight_check()
    x = input(sec.repr_mess("enter_comm", "r"))
    commands = {
        "chooseloc": sec.me["diff"].choose_loc,
        "wait": wait,
        "avalocs": sec.me["diff"].print_ava_locs,
        "combat": sec.me["diff"].print_combat,
        "i": sec.me["diff"].print_inv,
        "health": sec.me["diff"].print_health,
        "heal": sec.me["diff"].heal,
        "exit": sec.me["diff"].exit,
        "h": sec.me["diff"].print_hint,
    }
    if x in commands:
        commands[x]()
    else:
        sec.repr_mess("invalid_comm", "p")


def talk_check():
    """
    Kontroluje, zda hráč neinicioval rozhovor
    """
    talk_locs = [
        "market",
        "chief",
        "alchemist",
        "alchemist2",
        "alchemist3",
        "alb",
        "altar",
    ]
    if sec.me["diff"].loc in talk_locs:
        sec.me["diff"].talking = True
        while sec.me["diff"].talking:
            talk()


def talk():
    """
    Ukládá hráčovi možnosti pokračování v rozhovoru do proměnné 'me_opts'
    Umožňuje hráči vstup podle výstupu z funkce talked_to()
    Rozhoduje, co se bude dít na základě hodnoty hráčova vstupu
    """
    me_opts = sec.locs_list[sec.me["diff"].loc].opts
    talked_to()
    inpt = input(sec.repr_mess("talk_inpt", "r"))
    back_locs = ["village", "prison", "chapel"]

    if me_opts.get(inpt) in back_locs:
        sec.me["diff"].loc = sec.me["diff"].last_loc
        sec.me["diff"].talking = False
    elif me_opts.get(inpt) == "trade":
        talk_trade()
    elif inpt in me_opts:
        sec.me["diff"].loc = me_opts.get(inpt)
    else:
        try:
            int(inpt)
            sec.repr_mess("invalid_opt", "p")
        except ValueError:
            sec.repr_mess("int_error", "p")
        talk()


def talked_to():
    """
    Vypisuje rozhovor na základě hráčově pozici v něm
    Ukládá do booleanů informace,
    zda se hráč dostal do potřebných částí rozhovoru
    (na základě kterých se volá jiný rozhovor ze stejné lokace)
    """
    sec.repr_loc("mess", sec.me["diff"].loc, "p")

    if sec.me["diff"].loc == "alchemtalk4":
        sec.npcs_for_loc["alchemist"].talked_to1 = True
    elif sec.me["diff"].loc == "alb":
        sec.npcs_for_loc["prison"].talked_to1 = True


def talk_trade():
    """
    Iniciuje obchodování na základě hráčovy lokace
    """
    if sec.me["diff"].loc == "alchemist2":
        trade(sec.npcs_for_loc["alchemist"])
    else:
        trade(sec.npcs_for_loc[sec.me["diff"].loc])

    if not sec.me["diff"].loc == "altar":
        sec.me["diff"].loc = sec.me["diff"].last_loc
    sec.me["diff"].talking = False


def trade(npc):
    """
    Iniciuje obchod jako takový
    Kontroluje, zda se hráč nachází v lokaci, která je spojená s hlavním úkolem
    a zda již hráč odevzdal úkolový předmět v této lokaci
    """
    if sec.me["diff"].loc == "alchemist2":
        alchem_chapel_trade(npc)
        item = "Sargelaz's head"

        if npc.inv[item] == sec.items_list[item].alchem_limit:
            sec.me["diff"].inv["Shard of Alberimus"] += 1
            sec.repr_mess("alchem_shard", "p")
            npc.talked_to2 = True
            sec.connect_locs()

    elif sec.me["diff"].loc == "altar":
        alchem_chapel_trade(npc)
        item1 = "void talon"
        item2 = "abyssal scope"
        item3 = "shadow blade"

        if (
            npc.inv[item1] == sec.items_list[item1].chapel_limit
            and npc.inv[item2] == sec.items_list[item2].chapel_limit
            and npc.inv[item3] == sec.items_list[item3].chapel_limit
        ):
            sec.me["diff"].inv["Zandalar's staff"] += 1
            sec.repr_mess("staff_obt", "p")
            npc.talked_to1 = True
        sec.me["diff"].loc = "chapel"
    else:
        buy_or_sell()


def alchem_chapel_trade(npc):
    """
    Podle hráčovy lokace určí proměnné, podle kterých kontroluje,
    zda hráč naplnil limit úkolových předmětů v této lokaci
    """
    sec.me["diff"].safe = 1

    for item in npc.inv:
        if sec.me["diff"].loc == "alchemist2":
            invalid_item = "Shard of Alberimus"
            limit = sec.items_list[item].alchem_limit
            mess = sec.repr_mess("alchem_give", "r")
        else:
            invalid_item = "Zandalar's staff"
            limit = sec.items_list[item].chapel_limit
            mess = sec.repr_mess("chapel_give", "r")

        if not item == invalid_item:
            if sec.me["diff"].inv[item] > 0 and not npc.inv[item] == limit:
                alchem_chapel_trade2(npc, item, limit, mess)

            elif sec.me["diff"].inv[item] == 0 and sec.me["diff"].safe == 1:
                sec.repr_mess("give_nothing", "p")
                sec.me["diff"].safe += 1


def alchem_chapel_trade2(npc, item, limit, mess):
    """
    Podle proměnné limit určuje počet předmětů k výměně, provádí jejich výměnu
    """
    if sec.me["diff"].inv[item] <= limit:
        x = sec.me["diff"].inv[item] - npc.inv[item]
    else:
        x = limit - npc.inv[item]

    npc.inv[item] += x
    sec.me["diff"].inv[item] -= x
    print(mess.format(sec.items_list[item].name))


def buy_or_sell():
    """
    Ptá se hráče, zda chce nakupovat, či prodávat
    """
    bln = input(sec.repr_mess("buy_or_sell", "r"))

    if bln == "1":
        sec.me["diff"].way = "buy"
    elif bln == "2":
        sec.me["diff"].way = "sell"
    else:
        try:
            int(bln)
            sec.repr_mess("invalid_opt", "p")
        except ValueError:
            sec.repr_mess("int_error", "p")
        buy_or_sell()

    buy_sell()


def buy_sell():
    """
    Ptá se hráče co chce nakoupit, či prodat
    """
    item = input(sec.repr_mess("market_item", "r").format(sec.me["diff"].way))

    if item in sec.me["diff"].inv:
        buy_sell2(item)
    else:
        if sec.me["diff"].way == "sell":
            sec.repr_mess("no_item", "p")
        else:
            sec.repr_mess("no_buy", "p")
        buy_sell()

    cont_trading()


def buy_sell2(item):
    """
    Kontroluje, zda je hráčův výběr možný
    """
    if sec.items_list[item].sellval == 0:
        print(sec.repr_mess("no_market", "r").format(sec.me["diff"].way))
    else:
        if sec.me["diff"].way == "buy":
            sec.me["diff"].buy(item)
        elif sec.me["diff"].way == "sell" and sec.me["diff"].inv.get(item) > 0:
            sec.me["diff"].sell(item)


def cont_trading():
    """
    Ptá se hráče, zda chce pokračovat v obchodování
    """
    x = input(sec.repr_mess("cont_trade", "r"))

    if x == "1":
        trade(sec.npcs_for_loc[sec.me["diff"].loc])
    elif x == "2":
        sec.me["diff"].loc = "village"
        sec.me["diff"].talking = False
    else:
        try:
            int(x)
            sec.repr_mess("invalid_opt", "p")
        except ValueError:
            sec.repr_mess("int_error", "p")

        cont_trading()


def fight_check():
    """
    Kontroluje hráčovu lokaci a iniciuje případný souboj
    podle proměnné chance, reprezentující šanci na potkání oponenta
    """
    if (
        sec.me["diff"].loc == "chapel"
        and sec.me["diff"].inv.get("Zandalar's staff") == 1
        and not sec.hostile_locs["bossfight"].defeated
    ):
        sec.repr_mess("pre_boss", "p")
        sec.me["diff"].loc = "bossfight"

    if sec.me["diff"].loc in sec.hostile_locs:
        ran = randint(1, 100)

        if ran < sec.hostile_locs[sec.me["diff"].loc].chance:
            fight_input(sec.hostile_locs[sec.me["diff"].loc])


def wait():
    """
    Pokud to je možné, iniciuje souboj
    """
    if sec.me["diff"].loc in sec.hostile_locs:
        fight_input(sec.hostile_locs[sec.me["diff"].loc])


def fight_input(enemy):
    """
    Umožňuje hráči reagovat na situace souboje
    """
    mess = sec.repr_mess("under_att", "r")
    print(mess.format(sec.me["diff"].name, enemy.name))
    fight(enemy)
    end_fight(enemy)


def fight(enemy):
    """
    Dokud jsou kameny na hrací ploše, nastavuje maximální
    a minimální možný počet kamenů k odebrání v jednom tahu AI,
    po kterém vypíše aktuální počet kamenů na hrací ploše
    Střídá tahy AI a hráče
    """
    while sec.me["diff"].n > 0:
        if not sec.me["diff"].on_turn:
            sec.me["diff"].min_take = 1
            sec.me["diff"].max_take = min(sec.me["diff"].n, 3)
            sec.me["diff"].n -= enemy.take()

            mess = sec.repr_mess("stones_on_board", "r")
            print(mess.format(sec.me["diff"].n))
            sec.me["diff"].on_turn = True
        else:
            user_turn()


def user_turn():
    """
    Nastavuje maximální a minimální počet kamenů k odebrání v jednom tahu hráče
    """
    if sec.me["diff"].inv.get("Zandalar's staff") > 0:
        sec.me["diff"].max_take = 4
        sec.me["diff"].min_take = 0

    sec.me["diff"].max_take = min(sec.me["diff"].n, sec.me["diff"].max_take)
    sec.me["diff"].take()
    sec.me["diff"].on_turn = False


def end_fight(enemy):
    """
    Koná podle toho, zda hráč souboj vyhrál, či ne
    Po hráčově výhře nad speciálním oponentem ho vyřadí z lokace,
    kde se protivník nacházel
    """
    if not sec.me["diff"].on_turn:
        sec.repr_mess("fight_won", "p")
        enemy.trophy()
        if enemy.name == "Sargelaz":
            sec.hostile_locs.pop("lair")
        elif enemy.name == "Zandalar":
            sec.hostile_locs["bossfight"].defeated = True
            sec.repr_mess("boss_def", "p")
            sec.me["diff"].loc = "village"
    else:
        print(sec.repr_mess("fight_lost", "r").format(enemy.harm))
        sec.me["diff"].health -= enemy.harm
    sec.me["diff"].n = 21
    sec.me["diff"].on_turn = False


main(sec.Me, sec.locs_list)
