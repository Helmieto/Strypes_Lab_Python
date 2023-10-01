import sqlite3
from sys import argv

"select count(*) from food where descript like '%Veal%'"

data_base = sqlite3.connect("migete-food.db")
cursor = data_base.cursor()

#queries
create_db_query = "CREATE TABLE IF NOT EXISTS food (code TEXT,descript TEXT,nmbr TEXT,nutname TEXT,retention TEXT)"

insert_query = "INSERT INTO food (code, descript, nmbr, nutname, retention) VALUES (?, ?, ?, ?, ?)"


def create_db():
    cursor.execute(create_db_query)


def fill_db(file_name):
    with open(file_name, "r") as food_data:
        lines = food_data.readlines()

    for line in lines:
        data = line.strip().split("~^~")
        data[0] = data[0][1:]
        args = data[:5]
        #print(args)
        cursor.execute(insert_query, args)


def execute_user_query(user_query):
    cursor.execute(user_query)
    print(cursor.fetchone())


create_db()
fill_db("retn5_dat.txt")

usr_query = argv[1]

execute_user_query(usr_query)

data_base.close()