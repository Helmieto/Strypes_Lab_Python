from tkinter import *
from tkinter import ttk
import Exceptions as EX
import Controller as CT



class Screen():
    def __init__(self, root):

        #main frames
        self.login_frame = Frame(root)
        self.player_frame = Frame(root)
        self.combat_frame = Frame(root)

        # LOGIN
        self.login_frame.pack(fill=BOTH, expand=True)

        # labels for login
        self.username_label = Label(self.login_frame, text="username:")
        self.pass_label = Label(self.login_frame, text="password:")
        self.email_label = Label(self.login_frame, text="email:")
        self.login_label = Label(self.login_frame, text="Have an account?")
        self.signin_label = Label(self.login_frame, text="No account?")

        # warnings for login
        self.name_warning = Label(self.login_frame, text="", foreground="red")
        self.pass_warning = Label(self.login_frame, text="", foreground="red")
        self.email_warning = Label(self.login_frame, text="", foreground="red")

        # entries for login
        self.username_entry = Entry(self.login_frame)
        self.pass_entry = Entry(self.login_frame, show="*")
        self.email_entry = Entry(self.login_frame)

        # buttons for login
        self.login_btn = Button(self.login_frame, text="Log in", command=self.show_log_in)
        self.enter_btn = Button(self.login_frame, text="Enter", command=self.log_in)
        self.signin_btn = Button(self.login_frame, text="Sign in", command=self.show_sign_in)
        self.complete_btn = Button(self.login_frame, text="Complete", command=self.sign_in)

        # visualizing
        self.populate_login()

        # PLAYER BOARD
        self.player = None
        self.curr_hero_idx = None
        self.heroes = []

        # COMBAT BOARD
        self.opponent = None
        self.opponent_hero_idx = None
        self.combat = None
        self.dmg_type = ""
        self.player_heroes = [] #stores buttons
        self.opponent_heroes = []#stores buttons
        self.combat_frame = Frame(root)
        self.combat_frame.rowconfigure(0, weight=1)
        self.combat_frame.rowconfigure(1, weight=1)
        self.combat_frame.rowconfigure(2, weight=1)

    def show_login_frame(self):
        self.login_frame.pack()

    def hide_login_frame(self):
        self.login_frame.pack_forget()

    def show_player_frame(self):
        self.player_frame.pack()
        self.trophy_label.config(text=f"{self.player.trophies} trophies")
        self.attacks_label.config(text=f"attacks left today: {self.player.attacks}")
        if self.player.attacks == 0:
            self.attack_btn.config(state="disabled")
        else:
            self.attack_btn.config(state="active")

    def hide_player_frame(self):
        self.player_frame.pack_forget()

    def show_combat_frame(self):
        self.combat_frame.pack()

    def hide_combat_frame(self):
        self.combat_frame.pack_forget()
        self.combat = None
        self.opponent = None
        self.opponent_hero_idx = None
        self.opponent_heroes = []
        self.player_heroes = []

    def populate_login(self):
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)

        self.pass_label.grid(row=1, column=0)
        self.pass_entry.grid(row=1, column=1)

        self.enter_btn.grid(row=2, column=1, columnspan=2)

        self.signin_label.grid(row=3, column=0)
        self.signin_btn.grid(row=3, column=1)

    def log_in(self):
        username = self.username_entry.get()
        password = self.pass_entry.get()

        try:
            self.player = CT.Player_factory(username, password)
            self.hide_login_frame()
            self.populate_player()
            self.show_player_frame()
            CT.update_db()

        except EX.Invalid_Username:
            self.name_warning.config(text="This username is wrong!")
            self.name_warning.grid(row=0, column=2)

        except EX.Invalid_Password:
            self.pass_warning.config(text="This password is wrong!")
            self.pass_warning.grid(row=1, column=2)

        except EX.Missing_Username:
            self.name_warning.config(text="Input username!")
            self.name_warning.grid(row=0, column=2)

        except EX.Missing_Password:
            self.pass_warning.config(text="Input password!")
            self.pass_warning.grid(row=1, column=2)

    def sign_in(self):
        username = self.username_entry.get()
        password = self.pass_entry.get()
        email = self.email_entry.get()

        try:
            CT.Player_sign_in(username, password, email)
            self.show_log_in()

        except EX.Taken_Username:
            self.name_warning.config(text="This username is already taken!")
            self.name_warning.grid(row=0, column=2)

        except EX.Missing_Username:
            self.name_warning.config(text="Input username!")
            self.name_warning.grid(row=0, column=2)

        except EX.Missing_Password:
            self.name_warning.config(text="Input password!")
            self.name_warning.grid(row=1, column=2)

        except EX.Missing_Email:
            self.name_warning.config(text="Input email!")
            self.name_warning.grid(row=2, column=2)

    def show_log_in(self):
        self.name_warning.grid_forget()
        self.pass_warning.grid_forget()
        self.email_warning.grid_forget()

        self.email_label.grid_forget()
        self.email_entry.grid_forget()
        self.complete_btn.grid_forget()
        self.login_label.grid_forget()
        self.login_btn.grid_forget()


        self.enter_btn.grid(row=2, column=0, columnspan=2)
        self.signin_label.grid(row=3, column=0)
        self.signin_btn.grid(row=3, column=1)

    def show_sign_in(self):
        self.name_warning.grid_forget()
        self.pass_warning.grid_forget()
        self.email_warning.grid_forget()

        self.enter_btn.grid_forget()
        self.signin_label.grid_forget()
        self.signin_btn.grid_forget()

        self.email_label.grid(row=2, column=0)
        self.email_entry.grid(row=2, column=1)

        self.complete_btn.grid(row=3, column=0, columnspan=2)

        self.login_label.grid(row=4, column=0)
        self.login_btn.grid(row=4, column=1)

    def exit(self):
        self.hide_player_frame()
        self.show_login_frame()
        self.player = None
        self.curr_hero_idx = None

    def populate_player(self):

        self.player_frame.columnconfigure(0, weight=1)
        self.player_frame.columnconfigure(1, weight=1)
        self.player_frame.columnconfigure(2, weight=1)

        self.board_frame = Frame(self.player_frame, borderwidth=20, bg="grey", relief="ridge")
        self.fill_heroes()


        self.stats_frame = Frame(self.player_frame, borderwidth=2, relief="ridge")
        self.stats_frame.grid(row=0, column=2, sticky="enws")



        self.hero_stats_frame = Frame(self.stats_frame, relief="ridge")
        self.hero_stats_frame.pack(fill=BOTH)

        self.hero_stats = Label(self.hero_stats_frame, text="HP:\nAP:\nLevel: ")
        self.upgrade_btn = Button(self.hero_stats_frame, text="Upgrade", command=self.upgrade_hero_stats)


        self.ability_1_frame = Frame(self.stats_frame, relief="ridge")
        self.ability_1_frame.pack(fill=BOTH)

        self.ability_1_stats = Label(self.ability_1_frame)
        self.ability_1_btn = Button(self.ability_1_frame, text="Upgrade",
                                    command=lambda abil_numb=1: self.upgrade_hero_ability(abil_numb))
        self.buy_ability1_btn = Button(self.ability_1_frame, text="Buy ability", command=lambda numb=1:self.buy_hero_ability(numb))

        self.ability_2_frame = Frame(self.stats_frame, relief="ridge")
        self.ability_2_frame.pack(fill=BOTH)

        self.ability_2_stats = Label(self.ability_2_frame)
        self.ability_2_btn = Button(self.ability_2_frame, text="Upgrade",
                                    command=lambda abil_numb=2: self.upgrade_hero_ability(abil_numb))
        self.buy_ability2_btn = Button(self.ability_2_frame, text="Buy ability", command=lambda numb=2:self.buy_hero_ability(numb))

        self.menu_frame = Frame(self.player_frame, borderwidth=2, relief="ridge")
        self.menu_frame.grid(row=1, column=0, columnspan=3)

        self.sell_btn = Button(self.menu_frame, text="Sell hero", command=self.sell_hero)
        self.buy_btn = Button(self.menu_frame, text="Buy hero", command=self.buy_hero)
        self.attack_btn = Button(self.menu_frame, text="Attack", command=self.show_combat_screen)
        self.exit_btn = Button(self.menu_frame, text="Exit", command=self.exit)

        self.trophy_label = Label(self.menu_frame, text=f"{self.player.trophies} trophies")
        self.money_label = Label(self.menu_frame, text=f"balance: {self.player.balance} $")
        self.attacks_label = Label(self.menu_frame, text=f"attacks left today: {self.player.attacks}")

        self.buy_btn.pack(side=LEFT)
        if self.player.heroes_cnt == 5:
            self.buy_btn.config(state="disabled")
        else:
            self.buy_btn.config(state="active")

        self.attack_btn.pack(side=LEFT)
        if self.player.attacks == 0:
            self.attack_btn.config(state="disabled")
        else:
            self.attack_btn.config(state="active")

        self.exit_btn.pack(side=LEFT)
        self.trophy_label.pack(side=LEFT)
        self.money_label.pack(side=LEFT)
        self.attacks_label.pack(side=LEFT)

    def fill_heroes(self):
        heroes_cnt = self.player.heroes_cnt
        for i in range(0, len(self.heroes)):
            self.heroes[i].grid_forget()


        for i in range(0, heroes_cnt):
            self.board_frame.columnconfigure(i, weight=1)

        self.board_frame.grid(row=0, column=0, columnspan=2, sticky="nesw")

        for i in range(0, heroes_cnt):
            hero_name = self.player.heroes[i].name
            self.hero_btn = Button(self.board_frame, text=hero_name, width=20, height=10,
                                   command=lambda hero_numb=i: self.show_hero_info(hero_numb))
            self.heroes.append(self.hero_btn)
            self.hero_btn.grid(row=0, column=i, sticky="ew")

    def visualize_hero_stats(self):
        hero_hp = self.player.heroes[self.curr_hero_idx].HP
        hero_ap = self.player.heroes[self.curr_hero_idx].AP
        hero_lvl = self.player.heroes[self.curr_hero_idx].level

        self.hero_stats.config(text=f"HP: {hero_hp}\nAP: {hero_ap}\nLevel: {hero_lvl}")
        self.hero_stats.pack(side=LEFT)
        self.upgrade_btn.pack(side=RIGHT)
        if hero_lvl == 10:
            self.upgrade_btn.config(state="disabled", text="Max level")
        else:
            self.upgrade_btn.config(state="active", text="Upgrade")
        self.sell_btn.pack(side=RIGHT)

    def visualize_hero_ability_stats(self, ability, number):
        ratio = ability.ratio
        lvl = ability.level
        tpe = ability.type()
        if number == 1:
            self.buy_ability1_btn.pack_forget()
            self.ability_1_stats.config(text=f"Type: {tpe}\nRatio: {ratio}\nLevel: {lvl}")
            self.ability_1_stats.pack(side=LEFT)
            self.ability_1_btn.pack(side=RIGHT)
            if lvl == 3:
                self.ability_1_btn.config(state="disabled", text="Max level")
            else:
                self.ability_1_btn.config(state="active", text="Upgrade")
        else:
            self.buy_ability2_btn.pack_forget()
            self.ability_2_stats.config(text=f"Type: {tpe}\nRatio: {ratio}\nLevel: {lvl}")
            self.ability_2_stats.pack(side=LEFT)
            self.ability_2_btn.pack(side=RIGHT)
            if lvl == 3:
                self.ability_2_btn.config(state="disabled", text="Max level")
            else:
                self.ability_2_btn.config(state="active", text="Upgrade")

    def hide_abilities_info(self):
        self.buy_ability1_btn.pack_forget()
        self.buy_ability2_btn.pack_forget()
        self.ability_1_btn.pack_forget()
        self.ability_1_stats.pack_forget()
        self.ability_2_btn.pack_forget()
        self.ability_2_stats.pack_forget()

    def hide_hero_info(self):
        self.hero_stats.pack_forget()
        self.upgrade_btn.pack_forget()
        self.hide_abilities_info()

    def show_hero_info(self, number):
        self.hide_abilities_info()

        self.curr_hero_idx = number
        self.visualize_hero_stats()

        if self.player.heroes[self.curr_hero_idx].ability_1 != None:

            self.visualize_hero_ability_stats(self.player.heroes[self.curr_hero_idx].ability_1, 1)
        else:
            self.buy_ability1_btn.pack(padx=20)

        if self.player.heroes[self.curr_hero_idx].ability_2 != None:

            self.visualize_hero_ability_stats(self.player.heroes[self.curr_hero_idx].ability_2, 2)

        else:
            self.buy_ability2_btn.pack(padx=20)

    def upgrade_hero_stats(self):

        try:
            self.player.upgrade_hero(self.curr_hero_idx)
            self.visualize_hero_stats()
            self.money_label.config(text=f"balance: {self.player.balance} $")

        except EX.Max_Level_Reached:
            pass

    def upgrade_hero_ability(self, number):
        if number == 1:
            try:
                self.player.upgrade_hero_ability(self.curr_hero_idx, 1)
                self.visualize_hero_ability_stats(self.player.heroes[self.curr_hero_idx].ability_1, 1)
                self.money_label.config(text=f"balance: {self.player.balance} $")
            except EX.Insufficient_Funds:
                pass
            except EX.Max_Level_Reached:
                pass
        else:
            try:
                self.player.upgrade_hero_ability(self.curr_hero_idx, 2)
                self.visualize_hero_ability_stats(self.player.heroes[self.curr_hero_idx].ability_2, 2)
                self.money_label.config(text=f"balance: {self.player.balance} $")
            except EX.Insufficient_Funds:
                pass
            except EX.Max_Level_Reached:
                pass

    def buy_hero_ability(self, number):
        popup = Toplevel()
        popup.title("Ability creator")

        label = Label(popup, text="Choose type:")
        label.pack()

        type_var = StringVar()
        combo = ttk.Combobox(popup, textvariable=type_var,
                             values=["Direct hit", "Spread shot", "Poison", "Heal", "Shield", "Block"])
        combo.pack()

        def get_selected_option():
            type_raw = type_var.get()
            type = ""

            if type_raw == "Direct hit":
                type = "direct"
            elif type_raw == "Spread shot":
                type = "spread"
            elif type_raw == "Poison":
                type = "poison"
            elif type_raw == "Heal":
                type = "heal"
            elif type_raw == "Shield":
                type = "shield"
            else :
                type = "block"

            popup.destroy()


            if number == 1:
                try:
                    self.player.buy_hero_ability(self.curr_hero_idx, 1, type)
                    self.visualize_hero_ability_stats(self.player.heroes[self.curr_hero_idx].ability_1, 1)
                    self.money_label.config(text=f"balance: {self.player.balance} $")
                except EX.Insufficient_Funds:
                    pass

            else:
                try:
                    self.player.buy_hero_ability(self.curr_hero_idx, 2, type)
                    self.visualize_hero_ability_stats(self.player.heroes[self.curr_hero_idx].ability_2, 2)
                    self.money_label.config(text=f"balance: {self.player.balance} $")
                except EX.Insufficient_Funds:
                    pass

        button = Button(popup, text="Choose", command=get_selected_option)
        button.pack()

    def sell_hero(self):
        self.player.sell_hero(self.curr_hero_idx)
        self.hide_hero_info()
        self.fill_heroes()
        self.money_label.config(text=f"balance: {self.player.balance} $")
        if self.player.heroes_cnt == 5:
            self.buy_btn.config(state="disabled")
        else:
            self.buy_btn.config(state="active")

    def buy_hero(self):

        try:
            self.player.buy_hero()
            self.fill_heroes()
            self.money_label.config(text=f"balance: {self.player.balance} $")
            if self.player.heroes_cnt == 5:
                self.buy_btn.config(state="disabled")
            else:
                self.buy_btn.config(state="active")
        except EX.Max_Heroes_Reached:
            pass
        except EX.Insufficient_Funds:
            pass

    def show_combat_screen(self):
        self.hide_player_frame()
        self.visualize_combat()

    def visualize_combat_stats_attacker(self, numb):
        self.ab1_btn_at.grid_forget()
        self.ab2_btn_at.grid_forget()

        self.curr_hero_idx = numb
        hero_AP = self.player.heroes[self.curr_hero_idx].AP
        ab1_ratio = 0
        ab2_ratio = 0

        if self.player.heroes[self.curr_hero_idx].ability_1 != None:
            ab1_ratio = self.player.heroes[self.curr_hero_idx].ability_1.ratio
            if self.player.heroes[self.curr_hero_idx].ability_1.type() == "direct hit":
                self.ab1_btn_at.config(text="direct hit")


            elif self.player.heroes[self.curr_hero_idx].ability_1.type() == "spread shot":
                self.ab1_btn_at.config(text="spread shot")


            elif self.player.heroes[self.curr_hero_idx].ability_1.type() == "poison":
                self.ab1_btn_at.config(text="poison")

            self.ab1_btn_at.grid(row=1, column=1)
            if self.player.heroes[self.curr_hero_idx].ability_1.cooldown == True:
                self.ab1_btn_at.config(state="disabled")
            else:
                self.ab1_btn_at.config(state="active")

        if self.player.heroes[self.curr_hero_idx].ability_2 != None:
            ab2_ratio = self.player.heroes[self.curr_hero_idx].ability_2.ratio
            if self.player.heroes[self.curr_hero_idx].ability_2.type() == "direct hit":
                self.ab2_btn_at.config(text="direct hit")


            elif self.player.heroes[self.curr_hero_idx].ability_2.type() == "spread shot":
                self.ab2_btn_at.config(text="spread shot")


            elif self.player.heroes[self.curr_hero_idx].ability_2.type() == "poison":
                self.ab2_btn_at.config(text="poison")

            self.ab1_btn_at.grid(row=1, column=2)
            if self.player.heroes[self.curr_hero_idx].ability_2.cooldown == True:
                self.ab2_btn_at.config(state="disabled")
            else:
                self.ab2_btn_at.config(state="active")

        self.at_stats.config(
            text=f"Basic attack damage: {hero_AP}\nAbility 1 damage: {ab1_ratio * hero_AP}\nAbility 2 damage: {ab2_ratio * hero_AP}")
        self.at_stats.grid(row=0, column=0, columnspan=3)
        self.basic_atck_at.grid(row=1, column=0)

    def visualize_combat_stats_defender(self, numb):
        self.opponent_hero_idx = numb
        hero_hp = self.opponent.heroes[numb].curr_hp
        hero_shield = self.opponent.heroes[numb].curr_shield
        poison = self.opponent.heroes[numb].poison_left

        self.df_stats.config(text=f"HP: {hero_hp}\nShield: {hero_shield}\nPoisened for {poison} turns")
        self.df_stats.pack(side=LEFT)

    def visualize_combat(self):

        self.opponent = CT.Find_oponent(self.player.name)
        self.player.use_attack()
        self.combat = CT.Combat(self.player, self.opponent)
        self.combat_frame.pack(fill=BOTH, expand=True)

        self.attacker_frame = Frame(self.combat_frame, borderwidth=20, bg="green", relief="ridge")
        self.defender_frame = Frame(self.combat_frame, borderwidth=20, bg="red", relief="ridge")

        for i in range(0, self.player.heroes_cnt):
            self.attacker_frame.columnconfigure(i, weight=1)
            self.btn = Button(self.attacker_frame, text=f"{self.player.heroes[i].name}", width=20, height=10,
                              command=lambda hero=i: self.visualize_combat_stats_attacker(hero))
            self.player_heroes.append(self.btn)
            self.btn.grid(row=0, column=i)

        for i in range(0, self.opponent.heroes_cnt):
            self.defender_frame.columnconfigure(i, weight=1)
            self.btn = Button(self.defender_frame, text=f"{self.opponent.heroes[i].name}", width=20, height=10,
                              command=lambda hero=i: self.visualize_combat_stats_defender(hero))
            self.opponent_heroes.append(self.btn)
            self.btn.grid(row=0, column=i)

        self.attacker_frame.grid(row=1, column=0)
        self.defender_frame.grid(row=0, column=0)

        self.attacker_info_frame = Frame(self.combat_frame, borderwidth=20, bg="grey", relief="ridge")
        self.defender_info_frame = Frame(self.combat_frame, borderwidth=20, bg="grey", relief="ridge")

        self.attacker_info_frame.grid(row=1, column=1)
        self.defender_info_frame.grid(row=0, column=1)

        self.at_stats = Label(self.attacker_info_frame, text="", width=20, height=10)
        self.df_stats = Label(self.defender_info_frame, text="", width=20, height=10)

        self.basic_atck_at = Button(self.attacker_info_frame, text="Basic attack",
                                    command=lambda dmg_tpe=0: self.assign_dmg_type(dmg_tpe))
        self.ab1_btn_at = Button(self.attacker_info_frame, text="", command=lambda dmg_tpe=1: self.assign_dmg_type(dmg_tpe))
        self.ab2_btn_at = Button(self.attacker_info_frame, text="", command=lambda dmg_tpe=2: self.assign_dmg_type(dmg_tpe))

        self.buttons_frame = Frame(self.combat_frame)
        self.buttons_frame.grid(row=2, column=0)

        self.attack_btn = Button(self.buttons_frame, text="Attack", width=10, command=self.initiate_attack)
        self.attack_btn.pack(side=LEFT)

        self.end_turn_btn = Button(self.buttons_frame, text="End Turn", width=10, command=self.end_turn)
        self.end_turn_btn.pack(side=LEFT)

        self.surrender_btn = Button(self.buttons_frame, text="Surrender", width=10, command=self.surrender)
        self.surrender_btn.pack(side=LEFT)

        self.turns_remaining = Label(self.buttons_frame, text=f"Remaining turns: {self.combat.turns_remaining}")
        self.turns_remaining.pack(side=RIGHT)

    def assign_dmg_type(self, number):

        if number == 0:
            self.dmg_type = "basic"

        elif number == 1:
            self.dmg_type = self.player.heroes[self.curr_hero_idx].ability_1.type()

        elif number == 2:
            self.dmg_type = self.player.heroes[self.curr_hero_idx].ability_2.type()

    def check_dead(self):
        for i in range(0, self.opponent.heroes_cnt):
            if self.opponent.heroes[i].is_killed == True:
                self.opponent_heroes[i].config(state="disabled")

    def initiate_attack(self):

        if self.dmg_type == "basic":
            self.combat.use_basic_attack(self.curr_hero_idx,self.opponent_hero_idx)


        elif self.dmg_type == "direct hit":
            self.combat.use_direct_hit(self.curr_hero_idx, self.opponent_hero_idx)


        elif self.dmg_type == "spread shot":
            self.combat.use_spread_shot(self.curr_hero_idx, self.opponent_hero_idx)


        elif self.dmg_type == "poison":
            self.combat.use_poison(self.curr_hero_idx, self.opponent_hero_idx)

        self.player_heroes[self.curr_hero_idx].config(state="disabled")
        self.player_heroes[self.curr_hero_idx].grid(row=0, column=self.curr_hero_idx)
        self.visualize_combat_stats_defender(self.opponent_hero_idx)
        self.check_dead()
        self.dmg_type = ""
        self.curr_hero_idx = None
        self.opponent_hero_idx = None

    def give_award(self):
        if self.combat.attacker_wins == True:
            self.player.win_fight()
            self.opponent.lose_fight()
            popup = Toplevel()
            popup.title("Message")

            label = Label(popup, text="You won!")
            label.pack()

            btn = Button(popup, text="Great!", command=popup.destroy)
            btn.pack()
        else:
            self.player.lose_fight()
            self.opponent.win_fight()
            popup = Toplevel()
            popup.title("Message")

            label = Label(popup, text="You lost!")
            label.pack()

            btn = Button(popup, text="Sad!", command=popup.destroy)
            btn.pack()

    def end_turn(self):
        self.combat.end_turn()
        self.turns_remaining.config(text=f"Turns remaining: {self.combat.turns_remaining}")
        for i in range(0, self.player.heroes_cnt):
            self.player_heroes[i].config(state="active")



        if self.combat.turns_remaining == 0 or self.combat.attacker_wins == True:
            self.give_award()
            self.hide_combat_frame()
            self.show_player_frame()

    def surrender(self):
        self.give_award()
        self.hide_combat_frame()
        self.show_player_frame()



root = Tk()
root.title("EGG HUNTER")

game = Screen(root)

root.mainloop()