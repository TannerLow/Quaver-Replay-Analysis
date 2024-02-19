import database
from playerdata import get_leaderboard_by_page
from time import sleep


db = database.open_db("db/leaderboard_4k.fs")
connection = database.get_connection(db)

num = 0
for i in range(1, 201):
    lb_page = get_leaderboard_by_page(i, 1)  # 1 means 4k
    for user in lb_page:
        print(f"Adding entry #{num} to 4k leaderboard:", database.insert_leaderboard_entry(connection, user))
        num += 1
    if num % 500 == 0:  # pack every 10 pages
        connection, db = database.pack(connection, db)
    sleep(3)

connection, db = database.pack(connection, db)  # extra time at the end to make sure

connection.close()
db.close()
