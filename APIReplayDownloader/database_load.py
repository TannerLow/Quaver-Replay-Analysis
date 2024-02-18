import database
from playerdata import get_leaderboard_by_page


db = database.open_db("db/testdb.fs")
connection = database.get_connection(db)

for i in range(0, 5):
    lb_page = get_leaderboard_by_page(i)
    for user in lb_page:
        database.insert_leaderboard_entry(user)
    sleep(1)

