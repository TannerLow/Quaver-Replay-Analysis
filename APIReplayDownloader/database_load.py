import database
import transaction
from playerdata import get_leaderboard_by_page
from time import sleep


db = database.open_db("db/leaderboard_4k.fs")
connection = database.get_connection(db)

num = 0
for i in range(0, 1):
    lb_page = get_leaderboard_by_page(i, 1)  # 1 means 4k
    transaction.begin()
    for user in lb_page:
        print(f"Adding entry #{num} to 4k leaderboard:", database.insert_leaderboard_entry(connection, user))
        num += 1
    transaction.commit()
    if num >= 1250:  # pack every 25 pages
        connection, db = database.pack_db(connection, db)
        print("Packing db...")
        num = 0
    sleep(2)

connection, db = database.pack_db(connection, db)  # extra time at the end to make sure

connection.close()
db.close()
