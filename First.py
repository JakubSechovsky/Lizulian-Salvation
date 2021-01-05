# importuje knihovny random a json a druhý soubor (Second.py) pod zkratkou sec
import random
import json
import Second as sec


class Enemy:  # definuje třídu Enemy (nepřítel) a její atributy
    def __init__(self, loc, loot, name, chance, harm, low_limit, up_limit, best_act, defeated):
        self.loot = loot
        self.loc = loc
        self.name = name
        self.chance = chance
        self.harm = harm
        self.low_limit = low_limit
        self.up_limit = up_limit
        self.best_act = best_act
        self.defeated = defeated
        self.best_score = -float("inf")

    # určuje podle jaké metody bude hráčův oponent brát kameny z hrací plochy
    def take(self):
        # pokud je jméno hráčova oponenta "Sargelaz", AI bude hrát s metodou simulationAI()
        if self.name == "Sargelaz":
            x = self.simulationAI()
        # pokud hráč nevlastní věc jménem "Zandalar's staff", metoda je určena obtížností, jakou si hráč na začátku hry navolil (1 / lehká - randomAI(); 2 / střední, 3 / těžká - simulationAI())
        elif not sec.me.inv.get("Zandalar's staff") > 0:
            ai = {"1": self.randomAI, "2": self.simulationAI,
                  "3": self.simulationAI}
            x = ai[sec.me.diff]()
        # pokud hráč vlastní věc jménem "Zandalar's staff" každý jeho oponent bude brát kameny podle metody perfectAI() (oponenta jménem "Sargelaz" hráč po získání "Zandalar's staff" nepotká)
        else:
            x = self.perfectAI()
        # vypíše počet kamenů odebraných pomocí vybrané metody a vrátí ho
        print(sec.repr_mess("enemy_take", "r").format(self.name, x))
        return x

    def randomAI(self): return random.randint(  # "nejlehčí" AI, dělá náhodný tah ze všech možných tahů
        sec.me.min_take, sec.me.max_take)

    # vrátí číslo vybrané na základě simulace tahů hráče (metoda Monte Carlo), pro každý možný tah, kdy je AI na řadě
    def simulationAI(self):
        self.best_act = -1
        self.best_score = -float("inf")
        for x in range(sec.me.min_take, sec.me.max_take + 1):
            act_score = 0
            self.simulationAI2(x, act_score)
        return self.best_act

    # vlastní simulace jako taková
    def simulationAI2(self, x, act_score):
        # čím větší číslo v range, tím je AI přesnější a výrazně pomalejší (časová složitost n^2)
        for _ in range(1000):
            stone_count = sec.me.n - x
            ai_turn = False
            while stone_count > 0:
                stone_count -= min(stone_count,
                                   random.randint(sec.me.min_take, sec.me.max_take + 1))
                # simulace střídání hráče a AI
                ai_turn = not ai_turn
            # act_score určuje, zda jednu danou simulaci (jednu iteraci for cyklu) AI vyhrála (+1), či ne (-1)
            if ai_turn:
                act_score -= 1
            else:
                act_score += 1
        # každá možnost AI (proměnná x) má jiné act_score, funkce vrátí x s největším act_score (proměnná self.best_score)
        if act_score > self.best_score:
            self.best_score = act_score
            self.best_act = x

    def perfectAI(self):
        # sety čísel, ze kterých hráč může vyhrát - w_nums a ta, ze kterých hráč prohraje (při správných výstupech AI) - l_nums
        l_nums = set([])
        w_nums = set([])
        # do setů rozdělí všechna čísla od 0 po aktuální počet kamenů (me.n)
        for x in range(0, sec.me.n + 1):
            for i in range(sec.me.min_take, sec.me.max_take + 1):
                if x - i in l_nums:
                    w_nums.add(x)
            if x not in w_nums:
                l_nums.add(x)
        # každou ze svých možností otestuje, a pokud je rozdíl aktuálního počtu kamenů a aktuální možnosti (me.n - i) v setu l_nums, vrátí aktuální možnost
        for i in range(sec.me.min_take, sec.me.max_take + 1):
            if sec.me.n - i in l_nums:
                return(i)
        # pokud se stane, že je aktuální počet kamenů v l_nums, a hráčův oponent je na tahu, AI vrátí hodnotu vygenerovanou pomocí simulationAI()
        # čímž nechává hráči nejvíce místa k udělání chyby
        return self.simulationAI()

    # pokud hráč vyhraje nad oponentem, zavolá se tato metoda, která vygeneruje náhodné číslo (ran) z intervalu čísel, která jsou daná v enms.json souboru
    def trophy(self):
        ran = random.randint(self.low_limit, self.up_limit)
        # pokud je vygenerované číslo (ran) 0, vypíše zprávu, že hráč za výhru nic nedostal, pro jakékoliv jiné číslo zavolá metodu trophy2(ran)
        if ran == 0:
            sec.repr_mess("no_offer", "p")
        else:
            self.trophy2(ran)

    def trophy2(self, ran):
        # pro oponenta, jehož jméno (self.name) není "Sargelaz" vypíše zprávu, že mu oponent mu nabízí kořist, kterou z něj hráč může získat a zavolá metodu trophy_input(ran)
        if not self.name == "Sargelaz":
            print(sec.repr_mess("offer", "r").format(ran, self.loot))
            self.trophy_input(ran)
        # pro oponenta, jehož jméno (self.name) je "Sargelaz" vypíše zprávu, že hráč obdržel kořist, kterou z něj může obdržet a přidá ji do hráčova inventáře
        # hráč nemá na výběr odmítnout tuto kořist, protože by pak nemohl hru dohrát
        else:
            sec.repr_mess("sarg_loot", "p")
            sec.me.inv[self.loot] += ran

    def trophy_input(self, ran):
        # vypíše zprávu, zda chce hráč nabízenou kořist přijmout či odmítnout jako input
        x = input(
            sec.repr_mess("loot", "r"))
        # na základě vstupu hráče dělá následující: "1" - přidá kořist do hráčova inventáře a vypíše o tom zprávu, "2" - vypíše zprávu, že hráč odmítl oponentovu nabídku kořisti
        if x == "1":
            sec.me.inv[self.loot] += ran
            print(sec.repr_mess("received", "r").format(
                ran, self.loot))
        elif x == "2":
            print(sec.repr_mess("rejected", "r").format(
                ran, self.loot))
        # pro jakékoliv jiné číslo vypíše zprávu o neplatném vstupu, pro jakýkoliv jiný vstup požádá hráče, aby napsal číslo, v obou případech se zavolá rekurzivně zpátky
        else:
            try:
                int(x)
                sec.repr_mess("invalid_opt", "p")
            except ValueError:
                sec.repr_mess("int_error", "p")
            self.trophy()


def main(Me, locs_list):  # hlavní funkce hry, volá funkce na načtení dat z vedlejších .json souborů, bere si za argumenty třídu Me a slovník locs_list ze souboru Second.py
    load_json()
    # ukládá hráčovo jméno do proměnné me.name
    sec.me.name = input(sec.repr_mess("choose_name", "r"))
    # hráč si vybere obtížnost podle metody choose_difficulty() třídy Me
    sec.me.choose_difficulty()
    # vypíše úvod do hry
    sec.me.print_intro()
    # hlavní cyklus hry
    while sec.me.run:
        # kontroluje, zda má hráč nezáporný počet životů, pokud ano, vypíše zprávu o jeho herní smrti a nastaví boolean, podle kterého cyklus běží na False
        if sec.me.health <= 0:
            sec.repr_mess("dead", "p")
            sec.me.run = False
        # pokud je hráč "naživu" zavolá funkci user_input(Me, locs_list), jinak vypíše zprávu o konci hry
        if sec.me.run:
            user_input(Me, locs_list)
        else:
            sec.repr_mess("end", "p")


def load_json():  # dává dohromady funkce na načítání dat z .json souborů
    load_enms()
    sec.load_locs()
    sec.load_npcs()


def load_enms():  # načítá oponenty z enms.json a ukládá je jako instance třídy Enemy do slovníku hostile_locs v souboru Second.py podle lokace, ve které se nacházejí
    with open("./enms.json", "r", encoding="utf-8") as enms_file:
        enms = json.load(enms_file)
        for enm in enms:
            atts = enms[enm]
            new_enm = Enemy(atts["loc"], atts["loot"], atts["name"],
                            atts["chance"], atts["harm"], atts["low_limit"], atts["up_limit"], atts["best_act"], atts["defeated"])
            sec.hostile_locs[atts["loc"]] = new_enm


def user_input(Me, locs_list):  # umožňuje hráči psát příkazy sepsané ve slovníku commands
    # kontroluje, zda hráč není v lokaci, kde má mluvit s jinou (hráčem neovladatelnou) postavou (pokud ano, iniciuje rozhovor)
    talk_check()
    # vypíše zprávu pro lokaci, ve které se hráč právě nachází
    sec.repr_loc("mess", sec.me.loc, "p")
    # pokud se hráč nachází v lokaci, kde může s někým / něčím bojovat, pak na základě náhody (ne)iniciuje souboj s nepřítelem
    fight_check()
    # dává hráči možnost napsat příkaz, podle kterého, pokud je ve slovníku commands, vykoná příslušnou funkci (metodu třídy Me)
    x = input(sec.repr_mess("enter_comm", "r"))
    commands = {"chooseloc": sec.me.choose_loc, "wait": wait, "avalocs": sec.me.print_ava_locs, "combat": sec.me.print_combat,
                "i": sec.me.print_inv, "health": sec.me.print_health, "heal": sec.me.heal, "exit": sec.me.exit, "h": sec.me.print_hint}
    if x in commands:
        commands[x]()
    # pokud hráčův příkaz ve slovníku commands není, vypíše chybovou hlášku (a zavolá se znovu díky while cyklu ve funkci main(Me, locs_list))
    else:
        sec.repr_mess("invalid_comm", "p")


def talk_check():  # pokud je hráč v lokaci, kde má s někým mluvit, iniciuje rozhovor (funkce talk())
    tlk = ["market", "chief", "alchemist",
           "alchemist2", "alchemist3", "alb", "altar"]
    if sec.me.loc in tlk:
        sec.me.talking = True
        while sec.me.talking:
            talk()


def talk():  # ukládá hráčovi možnosti do slovníku me_opts, hráčova poslední lokace (me.last_loc) se nemění, aby se mohl hráč vrátit z rozhovoru
    me_opts = sec.repr_loc(sec.me.loc, "opts", "r")
    talked_to()
    # umožňuje hráči vstup, pokud je vstup v možnostech pro hráčovu aktuální lokaci (slovník me_opts), přenese na vybrané místo
    inpt = input(sec.repr_mess("talk_inpt", "r"))
    back_locs = ["village", "prison", "chapel"]
    # pokud je hodnota hráčova vstupu ve slovníku me_opts i v listu back_locs, přesune ho na jeho poslední lokaci a ukončí while cyklus ve vunkci talk_check()
    if me_opts.get(inpt) in back_locs:
        sec.me.loc = sec.me.last_loc
        sec.me.talking = False
    # pokud je hodnota hráčova vstupu ve slovníku me_opts "trade", iniciuje přechod k obchodování (funkci talk_trade())
    elif me_opts.get(inpt) == "trade":
        talk_trade()
    # pokud je hráčův vstup v možnostech jeho lokace, přesune ho na hodnotu jeho vstupu ve slovníku me_opts
    elif inpt in me_opts:
        sec.me.loc = me_opts.get(inpt)
    # pro vstup jiný, než číslo, požádá hráče, aby zadal číslo, pokud hráč zadá jiné číslo, než mu bylo nabídnuto ve funkci talked_to() (řádek 223), vypíše chybovou hlášku
    # v obou případech se zavolá rekurzivně znovu
    else:
        try:
            int(inpt)
            sec.repr_mess("invalid_opt", "p")
        except ValueError:
            sec.repr_mess("int_error", "p")
        talk()


def talked_to():  # vypíše zprávu pro hráčovu lokaci (rozhovor) nastavuje booleany lokací podle toho, zda hráč určité lokace navštívil (kam se až v rozhovoru dostal)
    sec.repr_loc("mess", sec.me.loc, "p")
    if sec.me.loc == "alchemtalk4":
        sec.npcs_for_loc["alchemist"].talked_to1 = True
    elif sec.me.loc == "alb":
        sec.npcs_for_loc["prison"].talked_to1 = True


def talk_trade():  # iniciuje obchod podle lokace hráče
    # pokud je hráčova lokace v rozhovoru "alchemist2", iniciuje obchod s postavou v lokaci "alchemist"
    if sec.me.loc == "alchemist2":
        trade(sec.npcs_for_loc["alchemist"])
    # pro všechny ostatní lokaci inciuje obchod s postavou v hráčově lokaci
    else:
        trade(sec.npcs_for_loc[sec.me.loc])
    # pokud hráčova lokace není "altar", vrací ho na jeho poslední lokaci a ukončuje while cyklus ve funkci talk_check()
    if not sec.me.loc == "altar":
        sec.me.loc = sec.me.last_loc
    sec.me.talking = False


def trade(npc):  # iniciuje samotný obchod
    # pokud je hráč v lokaci "alchemist2", zavolá funkci alchem_trade(npc) a kontroluje, zda hráč odevzdal postavě úkolový předmět
    # pokud ano, hráči se do inventáře přidá odměna za splněný úkol, vypíše se o tom zpráva, nastaví se boolean, že hráč úkol splnil (aby ho nemohl splnit vícekrát) a přidá novou lokaci pomocí funkce connect_loc() v souboru Second.py
    if sec.me.loc == "alchemist2":
        alchem_trade(npc)
        if npc.inv["Sargelaz's head"] == sec.items_list["Sargelaz's head"].alchem_limit:
            sec.me.inv["Shard of Alberimus"] += 1
            sec.repr_mess("alchem_shard", "p")
            npc.talked_to2 = True
            sec.connect_locs()
    # pokud je hráč v lokaci "altar", zavolá funkci chapel_trade(npc) a kontroluje, zda hráč odevzdal v lokaci všechny předměty, které odevzdat měl, na konec nastavuje hráčovu lokaci na "chapel"
    # pokud ano, hráči se přidá odměna za splněný úkol, vypíše se o tom zpráva a nastaví se boolean, že hráč úkol splnil
    elif sec.me.loc == "altar":
        chapel_trade(npc)
        if npc.inv["void talon"] == sec.items_list["void talon"].chapel_limit and npc.inv["abyssal scope"] == sec.items_list["abyssal scope"].chapel_limit and npc.inv["shadow blade"] == sec.items_list["shadow blade"].chapel_limit:
            sec.me.inv["Zandalar's staff"] += 1
            sec.repr_mess("staff_obt", "p")
            npc.talked_to1 = True
        sec.me.loc = "chapel"
    # pro každou jinou hráčovu lokaci zavolá funkci buy_or_sell()
    else:
        buy_or_sell()


def alchem_trade(npc):  # zajišťuje, že hráč odevzdá postavě vše, co může; jako první nastaví pojistku me.safe na 1
    sec.me.safe = 1
    # pro každou věc v inventáři postavy (pokud věc není "Shard of Alberimus") zkontroluje, zda hráč danou věc má v inventáři alespoň jednou a zároveň, že postava danou věc stále potřebuje
    # pokud ano a ano, zavolá funkci alchem_trade2(npc, item), pokud hráč danou věc v inventáři nemá ani jednou, vypíše se o tom zpráva
    for item in npc.inv:
        if not item == "Shard of Alberimus":
            if sec.me.inv[item] > 0 and not npc.inv[item] == sec.items_list[item].alchem_limit:
                alchem_trade2(npc, item)
            elif sec.me.inv[item] == 0 and sec.me.safe == 1:
                sec.repr_mess("give_nothing", "p")
                sec.me.safe += 1


# zavolá se v případě, že hráč danou věc má a postava ji zároveň potřebuje
def alchem_trade2(npc, item):
    # pokud je počet dané věci v hráčově inventáři menší nebo roven počtu věcí, kolik jich postava potřebuje, počet věcí k předání (x) je roven rozdílu počtů věcí v inventáři hráče a postavy (v tomto pořadí)
    if sec.me.inv[item] <= sec.items_list[item].alchem_limit:
        x = sec.me.inv[item] - npc.inv[item]
    # pokud je to jakkoliv jinak, počet věcí k předání (x) je roven rozdílu počtu věcí, kolik jich postava potřebuje a počtu věcí v inventáři postavy
    else:
        x = sec.items_list[item].alchem_limit - npc.inv[item]
    # k inventáři postavy se přidá počet daných věcí, ten samý počet se odečte od inventáře hráče (pro tu samou věc) a vytiskne se zpráva o tom, co a kolik dané věci hráč postavě předal
    npc.inv[item] += x
    sec.me.inv[item] -= x
    print(sec.repr_mess("alchem_give", "r").format(
        sec.items_list[item].name))


def chapel_trade(npc):  # zajišťuje, že hráč na lokaci "altar" nechá, co může; jako první nastaví pojistku me.safe na 1
    sec.me.safe = 1
    # pro každou položku v inventáři lokace (postavy; pokud věc není "Zandalar's staff") zkontroluje, zda hráč danou věc má v inventáři alespoň jednou a zároveň, že lokace danou věc stále potřebuje
    # pokud ano a ano, zavolá funkci chapel_trade2(npc, item), pokud hráč danou věc v inventáři nemá ani jednou, vypíše se o tom zpráva
    for item in npc.inv:
        if not item == "Zandalar's staff":
            if sec.me.inv[item] > 0 and not npc.inv[item] == sec.items_list[item].alchem_limit:
                chapel_trade2(npc, item)
            elif sec.me.inv[item] == 0 and sec.me.safe == 1 and not npc.inv[item] == sec.items_list[item].chapel_limit:
                sec.repr_mess("give_nothing", "p")
                sec.me.safe += 1


# zavolá se v případě, že hráč danou věc má a lokace ji zároveň potřebuje
def chapel_trade2(npc, item):
    # pokud je počet dané věci v hráčově inventáři menší nebo roven počtu věcí, kolik jich lokace potřebuje, počet věcí k předání (x) je roven rozdílu počtů věcí v inventáři hráče a lokace (v tomto pořadí)
    if sec.me.inv[item] <= sec.items_list[item].chapel_limit:
        x = sec.me.inv[item] - npc.inv[item]
    # pokud je to jakkoliv jinak, počet věcí k předání (x) je roven rozdílu počtu věcí, kolik jich postava potřebuje a počtu věcí v inventáři lokace
    else:
        x = sec.items_list[item].chapel_limit - npc.inv[item]
    # k inventáři postavy se přidá počet daných věcí, ten samý počet se odečte od inventáře hráče (pro tu samou věc) a vytiskne se zpráva o tom, co a kolik dané věci hráč postavě předal
    npc.inv[item] += x
    sec.me.inv[item] -= x
    print(sec.repr_mess("chapel_give", "r").format(
        sec.items_list[item].name))


def buy_or_sell():  # nastaví proměnnou me.way podle vstupu hráče - zda chce v obchodu prodávat či nakupovat, při jiném vstupu, než je v inputu
    x = input(sec.repr_mess("buy_or_sell", "r"))
    if x == "1":
        sec.me.way = "buy"
    elif x == "2":
        sec.me.way = "sell"
    # vypíše chybovou hlášku podle toho, zda hráč napsal něco jiného, než číslo, nebo špatné číslo
    else:
        try:
            int(x)
            sec.repr_mess("invalid_opt", "p")
        except ValueError:
            sec.repr_mess("int_error", "p")
        buy_or_sell()
    buy_sell()


def buy_sell():  # ptá se uživatele, co chce prodat/ koupit (podle me.way), pokud je hráčův vstup validní, zavolá funkci buy_sell2(x), po jejím ukončení zavolá funkci cont_trading()
    x = input(sec.repr_mess("market_item", "r").format(sec.me.way))
    if x in sec.me.inv:
        buy_sell2(x)
    # pokud vstup validní není, na základě me.way vypíše chybovou hlášku a zavolá se rekurzivně zpátky
    else:
        if sec.me.way == "sell":
            sec.repr_mess("no_item", "p")
        else:
            sec.repr_mess("no_buy", "p")
        buy_sell()
    cont_trading()


def buy_sell2(x):  # pokud lze věc koupit (její hodnota sellval není rovna 0), podle me.way zavolá metody buy(x) a sell(x) (pokud hráč danou věc vlastní alespoň jednou) třídy Me
    if sec.items_list[x].sellval == 0:
        print(sec.repr_mess("no_market", "r").format(sec.me.way))
    else:
        if sec.me.way == "buy":
            sec.me.buy(x)
        elif sec.me.way == "sell" and sec.me.inv.get(x) > 0:
            sec.me.sell(x)


def cont_trading():  # ptá se hráče zda chce pokračovat v obchodu, pokud ano (1), zavolá funkci trade(), pokud ne (2), vrátí hráče na lokaci "village" a zastaví while cyklus ve funkci talk_check()
    x = input(
        sec.repr_mess("cont_trade", "r"))
    if x == "1":
        trade(sec.npcs_for_loc[sec.me.loc])
    elif x == "2":
        sec.me.loc = "village"
        sec.me.talking = False
    # vypíše chybovou hlášku podle toho, zda hráč napsal špatné číslo, nebo napsal něco jiného, než číslo
    else:
        try:
            int(x)
            sec.repr_mess("invalid_opt", "p")
        except ValueError:
            sec.repr_mess("int_error", "p")
        cont_trading()


def fight_check():  # iniciuje případný souboj
    # pokud je hráč v lokaci "chapel", má věc "Zandalar's staff" a nepřemohl ještě finálního oponenta, přesune hráče do lokace "bossfight" a vypíše o tom zprávu
    if sec.me.loc == "chapel" and sec.me.inv.get("Zandalar's staff") == 1 and not sec.hostile_locs["bossfight"].defeated:
        sec.repr_mess("pre_boss", "p")
        sec.me.loc = "bossfight"
    # pokud se hráč nachází v lokaci, kde může potkat oponenta, načte náhodné číslo od 1 do 100 a pokud je toto číslo menší, než číslo pro šanci na potkání oponenta (proměnná chance) iniciuje souboj s daným oponentem v hráčově lokaci
    if sec.me.loc in sec.hostile_locs:
        ran = random.randint(1, 100)
        if ran < sec.hostile_locs[sec.me.loc].chance:
            fight_input(sec.hostile_locs[sec.me.loc])


def wait():  # iniciuje souboj, pokud se hráč nachází v lokaci, ve které může narazit na nepřítele
    if sec.me.loc in sec.hostile_locs:
        fight_input(sec.hostile_locs[sec.me.loc])


# vypíše zprávu, že je hráč pod útokem volá postupně funkce fight(enemy) a end_fight(enemy, me)
def fight_input(enemy):
    print(sec.repr_mess("under_att", "r").format(sec.me.name, enemy.name))
    fight(enemy)
    end_fight(enemy)


def fight(enemy):  # dokud je aktuální počet kamenů (me.n) větší, než 0, střídá tahy AI a hráče
    while sec.me.n > 0:
        if not sec.me.on_turn:
            # nastavuje minimální a maximální možný počet kamenů k odebrání, zavolá metodu take() třídy Enemy, odečte to, co vrátila od aktuálního počtu kamenů
            sec.me.min_take = 1
            sec.me.max_take = min(sec.me.n, 3)
            sec.me.n -= enemy.take()
            # vypíše kolik kamenů zůstalo po tahu AI a nastaví tah na tah hráče pomocí booleanu me.on_turn
            print(sec.repr_mess("stones_on_board", "r").format(sec.me.n))
            sec.me.on_turn = True
        else:
            # hraje hráč, zavolá funkci user_turn()
            user_turn()


def user_turn():
    # pokud má hráč věc se jménem "Zandalar's staff", nastaví maximální a minimální počet kamenů k odebrání na 4 a 0 (v tomto pořadí), pokud ne, zůstanou tyto hodnoty nastavené z tahu AI (ta hraje vždy před hráčem)
    if sec.me.inv.get("Zandalar's staff") > 0:
        sec.me.max_take = 4
        sec.me.min_take = 0
    sec.me.max_take = min(sec.me.n, sec.me.max_take)
    # volá metodu take() třídy Me (třída hráče, v souboru Second.py), po jejím ukončení nastaví tah na tah AI
    sec.me.take()
    sec.me.on_turn = False


def end_fight(enemy):  # zavolá se, pokud je aktuální počet kamenů na nule
    # pokud hráč není na tahu na konci hry, vypíše zprávu, že vyhrál a zavolá metodu trophy() třídy Enemy
    if sec.me.on_turn == False:
        sec.repr_mess("fight_won", "p")
        enemy.trophy()
        # pokud je jméno oponenta "Sargelaz" odstraní jeho lokaci ("lair") z listu lokací, kde hráč může narazit na nepřátele
        if enemy.name == "Sargelaz":
            sec.hostile_locs.pop("lair")
        # pokud je jméno oponenta "Zandalar" nastaví boolean o přemožení tohoto oponenta na True (aby se tento souboj neopakoval), vypíše zprávu o dokončení hry a vrátí hráče na jednu z prvních lokací
        elif enemy.name == "Zandalar":
            sec.hostile_locs["bossfight"].defeated = True
            sec.repr_mess("boss_def", "p")
            sec.me.loc = "village"
    else:
        # pokud hráč je na tahu na konci hry, vypíše zprávu, že prohrál a o kolik přišel životů (počet závisí na číslu daném v souboru enms.json)
        print(sec.repr_mess("fight_lost", "r").format(enemy.harm))
        sec.me.health -= enemy.harm
    # resetuje aktuální počet kamenů na 21 a nastaví tah na tah AI (aby vždy začínala)
    sec.me.n = 21
    sec.me.on_turn = False


main(sec.Me, sec.locs_list)
