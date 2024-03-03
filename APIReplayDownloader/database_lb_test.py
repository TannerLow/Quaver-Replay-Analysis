import database

# db = database.open_db("db/players.fs")
# connection = database.get_connection(db)
#
# adb = database.open_db("db/testdb.fs")
# aconnection = database.get_connection(adb)

lb_4k = database.open_db("db/leaderboard_4k.fs")
connection_4k = database.get_connection(lb_4k)

print(database.get_leaderboard_entry(connection_4k, 1))

lb_4k.close()
connection_4k.close()

# player = database.get_player(connection, 175369)
# print(player)
#
# player = database.get_leaderboard_entry(aconnection, 1)
# print(player)
#
# connection.close()
# db.close()
#
# aconnection.close()
# adb.close()