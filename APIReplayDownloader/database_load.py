import database
from playerdata import get_leaderboard_by_page
from time import sleep


lb_db = database.open_db("db/leaderboard.fs")
connection = database.get_connection(db)

for i in range(0, 71):
    lb_page = get_leaderboard_by_page(i)
    for user in lb_page:
        print("Adding lb entry to database: ", database.insert_leaderboard_entry(connection, user))
    sleep(1)

connection.close()
lb_db.close()
