import database

db = database.open_db("db/players.fs")
connection = database.get_connection(db)

adb = database.open_db("db/testdb.fs")
aconnection = database.get_connection(adb)

player = database.get_player(connection, 175369)
print(player)

player = database.get_leaderboard_entry(aconnection, 1)
print(player)

connection.close()
db.close()