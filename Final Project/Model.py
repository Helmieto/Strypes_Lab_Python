import sqlite3
import bcrypt
import Exceptions as EX
import os
import random


users_table_query = '''CREATE TABLE IF NOT EXISTS Players 
                        (Username TEXT PRIMARY KEY, Password TEXT, Email TEXT, 
                        Eggs INTEGER, Money INTEGER, Points INTEGER, Attacks_left INT DEFAULT 5, Defences_left INT DEFAULT 5)'''

heroes_table_query = '''CREATE TABLE IF NOT EXISTS Heroes(Name TEXT PRIMARY KEY, Holder TEXT, Ability_1 TEXT,
                        Ability_1_Level INTEGER, Ability_2 TEXT, Ability_2_level INTEGER, Level INTEGER, 
                        FOREIGN KEY (Holder) REFERENCES Players(Username))'''


def create_tables(users_query, heroes_query):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute(users_query)
    cursor.execute(heroes_query)

    data_base.commit()
    data_base.close()


def username_exists(username):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("SELECT username FROM Players WHERE username=?", (username,))

    if cursor.fetchone():
        data_base.close()
        return True
    else:
        data_base.close()
        return False


def password_hasher(password):
    password_encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_encoded, salt)

    return hashed_password


def sign_new_player(username, password, email):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    if username_exists(username):
        raise EX.Taken_Username

    if username == "":
        raise EX.Missing_Username

    if password == "":
        raise EX.Missing_Password

    if email == "":
        raise EX.Missing_Email

    hash_password = password_hasher(password)

    cursor.execute("INSERT INTO Players VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (username, hash_password, email, 0, 3000, 1000, 5, 5))
    data_base.commit()
    data_base.close()


def login_player(username, password):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    if username == "":
        raise EX.Missing_Username

    if password == "":
        raise EX.Missing_Password

    if not username_exists(username):
        raise EX.Invalid_Username

    cursor.execute("SELECT Username, Password, Money, Points, Eggs, Attacks_left FROM Players WHERE username = ?", (username,))


    player_data = cursor.fetchone()
    stored_password = player_data[1]
    input_password = password.encode('utf-8')

    if not bcrypt.checkpw(input_password, stored_password):
        raise  EX.Invalid_Password

    data_base.close()

    return player_data


def add_eggs():
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("UPDATE Players SET eggs = eggs + 5")

    data_base.commit()
    data_base.close()


def convert_eggs():
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("SELECT username, eggs FROM Players")
    eggs_per_player = cursor.fetchall()

    for name, eggcnt in eggs_per_player:
        removed_eggs = eggcnt // 2
        new_eggs = eggcnt - removed_eggs
        money_to_add = removed_eggs * 100

        cursor.execute("UPDATE Players SET eggs = ? WHERE username = ?",(new_eggs,name))
        cursor.execute("UPDATE Players SET money = money + ? WHERE username = ?", (money_to_add, name))


    data_base.commit()
    data_base.close()


def reset_daily_attacks():
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("UPDATE Players SET Attacks_left = 5")
    cursor.execute("UPDATE Players SET Defences_left = 5")

    data_base.commit()
    data_base.close()

def use_attack(player_name):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("UPDATE Players SET Attacks_left = Attacks_left - 1 Where Username = ?", (player_name, ))

    data_base.commit()
    data_base.close()

def use_defence(player_name):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("UPDATE Players SET Defences_left = Defences_left - 1 Where Username = ?", (player_name,))

    data_base.commit()
    data_base.close()

def upgrade_hero(name):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("UPDATE Heroes SET Level = Level + 1 WHERE Name = ?", (name,))

    data_base.commit()
    data_base.close()

def upgrade_ability(name, number):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    if number == 1:
        cursor.execute("UPDATE Heroes SET Ability_1_Level = Ability_1_Level + 1 WHERE Name = ?", (name,))

    if number == 2:
        cursor.execute("UPDATE Heroes SET Ability_2_level = Ability_2_level + 1 WHERE Name = ?", (name,))

    data_base.commit()
    data_base.close()

def buy_ability(name, number, type):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    if number == 1:
        cursor.execute("UPDATE Heroes SET Ability_1_Level = 1, Ability_1 = ? WHERE Name = ?", (type, name))

    if number == 2:
        cursor.execute("UPDATE Heroes SET Ability_2_Level = 1, Ability_2 = ? WHERE Name = ?", (type, name))

    data_base.commit()
    data_base.close()


def add_hero(player_name, hero_name):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("INSERT into Heroes (Name, Holder, Level) values (?, ?, ?)", (hero_name, player_name, 1))

    data_base.commit()
    data_base.close()


def delete_hero(name):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("DELETE FROM Heroes WHERE Name = ?", (name,))

    data_base.commit()
    data_base.close()

def send_hero_data(holder):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("Select * from Heroes where Holder = ?", (holder,))

    all_heroes = cursor.fetchall()

    data_base.close()

    return all_heroes

def edit_balance(player_name, new_amount):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("Update Players Set Money = ? Where Username = ?", (new_amount, player_name))

    data_base.commit()
    data_base.close()

def edit_trophies(player_name, new_amount):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("Update Players Set Points = ? Where Username = ?", (new_amount, player_name))

    data_base.commit()
    data_base.close()

def edit_eggs(player_name, new_amount):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("Update Players Set Eggs = ? Where Username = ?", (new_amount, player_name))

    data_base.commit()
    data_base.close()


def send_oponent_data(username):
    data_base = sqlite3.connect("egg_hunter.db")
    cursor = data_base.cursor()

    cursor.execute("Select Points From Players Where Username = ?", (username, ))

    points = cursor.fetchone()[0]
    points_min = points - 100
    points_max = points + 100

    cursor.execute("select Username, Points, Eggs From Players where Points Between ? and ? and Username != ? and Defences_left > 0", (points_min, points_max, username))
    all_players_found = cursor.fetchall()

    if all_players_found:

        random_player_data = random.choice(all_players_found)
        data_base.close()
        return random_player_data
    else:
        cursor.execute("SELECT Username, Points, Eggs FROM Players WHERE Points > ? and Username != ? and Defences_left > 0Order by Points ASC LIMIT 1",
                       (points, username))
        oponent = cursor.fetchone()
        if oponent:

            data_base.close()
            return oponent
        else:
            cursor.execute(
                "SELECT Username, Points, Eggs FROM Players WHERE Points < ? and Username != ? and Defences_left > 0 Order by Points DESC LIMIT 1",
                (points, username))

            oponent = cursor.fetchone()
            data_base.close()
            return oponent