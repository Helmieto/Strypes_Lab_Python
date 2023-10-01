import Model as DB
import datetime
import Exceptions as EX
import Constants as C
from names_generator import generate_name

class Ability():
    def __init__(self, level):
        self.level = level
        self.cooldown = 0

    def go_on_cooldown(self):
        self.cooldown = 2

    def reduce_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def upgrade(self):
        if self.level >= 3:
            raise EX.Max_Level_Reached
        self.level += 1


class Direct_hit(Ability):
    def __init__(self, level):
        super().__init__(level)
        self.ratio = C.DIRECT_HIT_RATIOS[self.level - 1]

    def upgrade(self):
        super().upgrade()
        self.ratio = C.DIRECT_HIT_RATIOS[self.level - 1]

    def type(self):
        return "direct hit"


class Spread_shot(Ability):
    def __init__(self, level):
        super().__init__(level)
        self.ratio = C.SPREADSHOT_RATIOS[self.level - 1]

    def upgrade(self):
        super().upgrade()
        self.ratio = C.SPREADSHOT_RATIOS[self.level - 1]

    def type(self):
        return "spread shot"


class Poison(Ability):
    def __init__(self, level):
        super().__init__(level)
        self.ratio = C.POISON_RATIOS[self.level - 1]

    def upgrade(self):
        super().upgrade()
        self.ratio = C.POISON_RATIOS[self.level - 1]

    def type(self):
        return "poison"


class Heal(Ability):
    def __init__(self, level):
        super().__init__(level)
        self.ratio = C.HEAL_RATIOS[self.level - 1]

    def upgrade(self):
        super().upgrade()
        self.ratio = C.HEAL_RATIOS[self.level - 1]

    def type(self):
        return "heal"


class Shield(Ability):
    def __init__(self, level):
        super().__init__(level)
        self.ratio = C.SHIELD_RATIOS[self.level - 1]

    def upgrade(self):
        super().upgrade()
        self.ratio = C.SHIELD_RATIOS[self.level - 1]

    def type(self):
        return "shield"


class Block(Ability):
    def __init__(self, level):
        super().__init__(level)
        self.ratio = C.BLOCK_RATIOS[self.level - 1]

    def upgrade(self):
        super().upgrade()
        self.ratio = C.BLOCK_RATIOS[self.level - 1]

    def type(self):
        return "block"


def Ability_Factory(ability_type, level):
    if ability_type == "direct":
        return Direct_hit(level)

    if ability_type == "spread":
        return Spread_shot(level)

    if ability_type == "poison":
        return Poison(level)

    if ability_type == "heal":
        return Heal(level)

    if ability_type == "shield":
        return Shield(level)

    if ability_type == "block":
        return Block(level)


class Hero():
    def __init__(self, name, level, ability_1, ability_2):
        self.name = name
        self.level = level

        self.HP = C.HERO_BASE_HP_PER_LEVEL[level - 1]
        self.AP = C.HERO_BASE_AP_PER_LEVEL[level - 1]

        self.ability_1 = ability_1
        self.ability_2 = ability_2

        #BATTLE ORIENTED
        self.curr_hp = self.HP
        self.curr_shield = 0

        self.poison_left = 0
        self.poison_dmg = 0

        self.has_attacked = False
        self.is_killed = False

    def upgrade_stats(self):
        if(self.level >= 10):
            raise EX.Max_Level_Reached

        self.level += 1
        self.HP = C.HERO_BASE_HP_PER_LEVEL[self.level - 1]
        self.AP = C.HERO_BASE_AP_PER_LEVEL[self.level - 1]

        self.curr_hp = self.HP

        DB.upgrade_hero(self.name)

    def upgrade_ability(self, number):
        if number == 1:
            self.ability_1.upgrade()
            DB.upgrade_ability(self.name, 1)

        if number == 2:
            self.ability_2.upgrade()
            DB.upgrade_ability(self.name, 2)

    def buy_ability(self, number, type):
        if number == 1:
            self.ability_1 = Ability_Factory(type, 1)
            DB.buy_ability(self.name, 1, type)

        if number == 2:
            self.ability_2 = Ability_Factory(type, 1)
            DB.buy_ability(self.name, 2, type)

    def delete_hero(self):
        DB.delete_hero(self.name)
        #devisualize from view

    def attack(self):
        self.has_attacked = True

    def reset_turn(self):
        self.has_attacked = False
        if self.ability_1 != None:
            self.ability_1.reduce_cooldown()
        if self.ability_2 != None:
            self.ability_2.reduce_cooldown()

    def receive_heal(self, amount):
        if self.poison_left > 0:
            amount *= C.REDUCED_HEALING
        self.curr_hp += amount
        if self.curr_hp > self.HP:
            self.curr_hp = self.HP

    def receive_shield(self, amount):
        self.curr_shield += amount

    def take_damage(self, dmg):
        if self.ability_1 != None and self.ability_1.type() == "block":
            dmg *= self.ability_1.ratio
        elif self.ability_2 != None and self.ability_2.type() == "block":
            dmg *= self.ability_2.ratio

        if self.curr_shield > 0:
            if self.curr_shield >= dmg:
                self.curr_shield -= dmg
            else:
                hp_to_remove = dmg - self.curr_shield
                self.curr_shield = 0
                self.curr_hp -= hp_to_remove
        else:
            self.curr_hp -= dmg

        if self.curr_hp <= 0:
            self.is_killed = True

    def get_poisoned(self, poison_dmg):
        self.poison_left = 2
        self.poison_dmg = poison_dmg

    def get_poison_dmg(self):
        self.take_damage(self.poison_dmg)
        self.poison_left -= 1
        if self.poison_left == 0:
            self.poison_dmg = 0

    def reset_hero(self):
        self.curr_shield = 0
        self.curr_hp = self.HP

        self.poisoned = False
        self.poison_left = 0

        self.has_attacked = False
        self.is_killed = False


def Heroes_Factory(holder):
    all_data = DB.send_hero_data(holder) #return format [(name, holder, ab1, ab1_lvl, ab2, ab2_lvl, hero_lvl), ...]

    all_heroes = []
    size = len(all_data)

    for i in range(0, size):
        name = all_data[i][0]
        level = all_data[i][6]
        ability_1 = Ability_Factory(all_data[i][2], all_data[i][3])
        ability_2 = Ability_Factory(all_data[i][4], all_data[i][5])

        all_heroes.append(Hero(name, level, ability_1, ability_2))
    #print(all_heroes[0].name, all_heroes[0].level, all_heroes[0].ability_1.type(), all_heroes[0].ability_2.type())
    #print(all_heroes[1].name, all_heroes[1].level, all_heroes[1].ability_1.type(), all_heroes[1].ability_2.type())
    return all_heroes


class Player():
    def __init__(self, name, money, trophies, eggs, attacks, defences):
        self.name = name
        self.balance = money
        self.trophies = trophies
        self.eggs = eggs
        self.attacks = attacks
        self.defences = defences
        self.heroes = Heroes_Factory(self.name)[:]
        self.heroes_cnt = len(self.heroes)

    def buy_hero(self):
        if self.heroes_cnt >= 5:
            raise EX.Max_Heroes_Reached

        cost = C.HERO_BASE_UPGRADE_COST

        if self.balance < cost:
            raise EX.Insufficient_Funds

        self.balance -= cost
        hero_name = generate_name()
        new_hero = Hero(hero_name, 1, None, None)

        self.heroes_cnt += 1
        self.heroes.append(new_hero)
        DB.edit_balance(self.name, self.balance)
        DB.add_hero(self.name, hero_name)

    def sell_hero(self, hero_numb):
        self.heroes_cnt -= 1

        if hero_numb != 4:
            self.heroes[hero_numb], self.heroes[-1] = self.heroes[-1], self.heroes[hero_numb]
        self.heroes[-1].delete_hero()
        self.heroes.pop()
        self.balance += C.HERO_SELL_PRICE

        DB.edit_balance(self.name, self.balance)

    def upgrade_hero(self, hero_numb):
        cost = C.HERO_BASE_UPGRADE_COST

        if self.balance < cost:
            raise EX.Insufficient_Funds

        self.balance -= cost
        self.heroes[hero_numb].upgrade_stats()

        DB.edit_balance(self.name, self.balance)

    def upgrade_hero_ability(self, hero_numb, ability_numb):
        cost = C.ABILITY_UPGRADE_COST

        if self.balance < cost:
            raise EX.Insufficient_Funds

        self.balance -= cost
        self.heroes[hero_numb].upgrade_ability(ability_numb)
        DB.edit_balance(self.name, self.balance)

    def buy_hero_ability(self, hero_numb, ability_numb, type):
        cost = C.ABILITY_UPGRADE_COST

        if self.balance < cost:
            raise EX.Insufficient_Funds

        self.balance -= cost
        self.heroes[hero_numb].buy_ability(ability_numb, type)
        DB.edit_balance(self.name, self.balance)

    def win_fight(self):
        self.trophies += 25
        self.eggs += 20

        DB.edit_trophies(self.name, self.trophies)
        DB.edit_eggs(self.name,self.eggs)

    def lose_fight(self):
        self.trophies -= 25
        if self.trophies < 0:
            self.trophies = 0

        self.eggs -= 20
        if self.eggs < 0:
            self.eggs = 0

        DB.edit_trophies(self.name, self.trophies)
        DB.edit_eggs(self.name, self.eggs)

    def use_attack(self):
        self.attacks -= 1
        DB.use_attack(self.name)

    def use_defence(self):
        self.defences -= 1
        DB.use_defence(self.name)


def Player_factory(username, password):
    player_data = DB.login_player(username, password) #return format is (name, pass, money, trophies, eggs, attacks)
    return Player(player_data[0], player_data[2], player_data[3], player_data[4], player_data[5], None)


def Player_sign_in(username, password, email):
    DB.sign_new_player(username, password, email)


def Find_oponent(username):
    opponent_data = DB.send_oponent_data(username) #format is (name, points, eggs)
    opponent = Player(opponent_data[0], None, opponent_data[1], opponent_data[2], None, None)
    DB.use_defence(opponent_data[0])
    return opponent


def update_db():

    curr_date = datetime.date.today()
    curr_hour = datetime.datetime.now().hour

    file = open("last date", "r")

    last_date_year = file.read(4)
    last_date_month = file.read(3).replace("-", "")
    last_date_day = file.read(3).replace("-", "")
    last_date = datetime.date(int(last_date_year), int(last_date_month), int(last_date_day))


    last_hour = file.read(3).strip()
    file.close()

    hour_diff = int(curr_hour) - int(last_hour)
    days_diff = (curr_date - last_date).days


    if days_diff == 0:
        for i in range(0, hour_diff):
            DB.add_eggs()
    else:
        DB.reset_daily_attacks()
        remaining_hours = 23 - int(last_hour) #remaining hours to 00:00 from the last edited day
        for i in range(0, remaining_hours):
            DB.add_eggs()
        DB.convert_eggs()

        for i in range(0, days_diff - 1):
            for j in range(0,24):
                DB.add_eggs()
            DB.convert_eggs()

        for i in range(0, curr_hour):
            DB.add_eggs()

    file = open("last date", "w")
    file.write(str(curr_date))
    file.write(f" {curr_hour}")

    file.close()


class Combat():
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        self.turns_remaining = 5
        self.attacker_wins = False
        self.cast_defences()

    def cast_defences(self):
        for i in range(0, self.opponent.heroes_cnt):
            if self.opponent.heroes[i].ability_1 != None:
                type = self.opponent.heroes[i].ability_1.type()
                if type in ["heal", "shield"]:
                    if self.opponent.heroes[i].ability_1.cooldown == 0:
                        amount = self.opponent.heroes[i].ability_1.ratio * self.opponent.heroes[i].HP
                        if type == "heal":
                            self.opponent.heroes[i].receive_heal(amount)

                        if type == "shield":
                            self.opponent.heroes[i].receive_shield(amount)

                        self.opponent.heroes[i].ability_1.go_on_cooldown()
                        self.opponent.heroes[i].ability_1.reduce_cooldown()
                        if self.opponent.heroes[i].ability_2.cooldown > 0:
                            self.opponent.heroes[i].ability_2.reduce_cooldown()

                        continue
                    else:
                        self.opponent.heroes[i].ability_1.reduce_cooldown()

            if self.opponent.heroes[i].ability_2 != None:
                type = self.opponent.heroes[i].ability_2.type()
                if type in ["heal", "shield"]:
                    if self.opponent.heroes[i].ability_2.cooldown == 0:
                        amount = self.opponent.heroes[i].ability_2.ratio * self.opponent.heroes[i].HP
                        if type == "heal":
                            self.opponent.heroes[i].receive_heal(amount)
                        if type == "shield":
                            self.opponent.heroes[i].receive_shield(amount)
                        self.opponent.heroes[i].ability_2.go_on_cooldown()
                        self.opponent.heroes[i].ability_2.reduce_cooldown()

    def use_basic_attack(self, attacker_idx, defender_idx):
        dmg = self.player.heroes[attacker_idx].AP
        self.opponent.heroes[defender_idx].take_damage(dmg)
        #print("HP:", self.opponent.heroes[defender_idx].curr_hp, "SH:", self.opponent.heroes[defender_idx].curr_shield)
        self.player.heroes[attacker_idx].attack()

    def use_direct_hit(self, attacker_idx, defender_idx):
        if self.player.heroes[attacker_idx].ability_1.type() == "direct hit":
            dmg = self.player.heroes[attacker_idx].ability_1.ratio * self.player.heroes[attacker_idx].AP
            self.player.heroes[attacker_idx].ability_1.go_on_cooldown()
            #self.player.heroes[attacker_idx].ability_1.reduce_cooldown()
        else:
            dmg = self.player.heroes[attacker_idx].ability_2.ratio * self.player.heroes[attacker_idx].AP
            self.player.heroes[attacker_idx].ability_2.go_on_cooldown()
            #self.player.heroes[attacker_idx].ability_2.reduce_cooldown()
        #print("HP:", self.opponent.heroes[defender_idx].curr_hp, "SH:", self.opponent.heroes[defender_idx].curr_shield)
        self.opponent.heroes[defender_idx].take_damage(dmg)
        self.player.heroes[attacker_idx].attack()

    def use_spread_shot(self, attacker_idx, defender_idx):
        if self.player.heroes[attacker_idx].ability_1.type() == "spread shot":
            dmg = self.player.heroes[attacker_idx].ability_1.ratio * self.player.heroes[attacker_idx].AP
            self.player.heroes[attacker_idx].ability_1.go_on_cooldown()
            #self.player.heroes[attacker_idx].ability_1.reduce_cooldown()
        else:
            dmg = self.player.heroes[attacker_idx].ability_2.ratio * self.player.heroes[attacker_idx].AP
            self.player.heroes[attacker_idx].ability_2.go_on_cooldown()
            #self.player.heroes[attacker_idx].ability_2.reduce_cooldown()

        if self.opponent.heroes_cnt < 3:
            for i in range (0, self.opponent.heroes_cnt):
                self.opponent.heroes[i].take_damage(dmg)
        else:
            if defender_idx == 0:
                self.opponent.heroes[defender_idx].take_damage(dmg)
                self.opponent.heroes[defender_idx + 1].take_damage(dmg)
            elif defender_idx == self.opponent.heroes_cnt - 1:
                self.opponent.heroes[defender_idx].take_damage(dmg)
                self.opponent.heroes[defender_idx - 1].take_damage(dmg)
            else:
                self.opponent.heroes[defender_idx - 1].take_damage(dmg)
                self.opponent.heroes[defender_idx].take_damage(dmg)
                self.opponent.heroes[defender_idx + 1].take_damage(dmg)
        self.player.heroes[attacker_idx].attack()
        #("HP:", self.opponent.heroes[defender_idx].curr_hp, "SH:", self.opponent.heroes[defender_idx].curr_shield)

    def use_poison(self, attacker_idx, defender_idx):
        if self.player.heroes[attacker_idx].ability_1.type() == "poison":
            dmg = self.player.heroes[attacker_idx].ability_1.ratio * self.player.heroes[attacker_idx].AP
            self.player.heroes[attacker_idx].ability_1.go_on_cooldown()
            #self.player.heroes[attacker_idx].ability_1.reduce_cooldown()
        else:
            dmg = self.player.heroes[attacker_idx].ability_2.ratio * self.player.heroes[attacker_idx].AP
            self.player.heroes[attacker_idx].ability_2.go_on_cooldown()
            #self.player.heroes[attacker_idx].ability_2.reduce_cooldown()

        self.opponent.heroes[defender_idx].take_damage(dmg)
        self.opponent.heroes[defender_idx].get_poisoned(dmg)
        self.player.heroes[attacker_idx].attack()
        #print("HP:", self.opponent.heroes[defender_idx].curr_hp, "SH:", self.opponent.heroes[defender_idx].curr_shield)

    def apply_poison_dmg(self):
        for i in range(0, self.opponent.heroes_cnt):
            if self.opponent.heroes[i].poison_left > 0:
                self.opponent.heroes[i].get_poison_dmg()

    def reset_heroes_attack_var(self):
        for i in range(0, self.player.heroes_cnt):
            self.player.heroes[i].reset_turn()

    def reset_heroes_after_end(self):
        for i in range(0, self.player.heroes_cnt):
            self.player.heroes[i].reset_hero()

        for i in range(0, self.opponent.heroes_cnt):
            self.opponent.heroes[i].reset_hero()

    def check_win(self):
        for i in range(0, self.opponent.heroes_cnt):
            if not self.opponent.heroes[i].is_killed:
                return
        self.attacker_wins = True

    def end_turn(self):
        self.cast_defences()
        self.apply_poison_dmg()
        self.reset_heroes_attack_var()
        self.turns_remaining -= 1
        self.check_win()