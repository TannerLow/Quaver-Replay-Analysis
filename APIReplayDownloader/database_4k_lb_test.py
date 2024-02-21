import database

db = database.open_db("db/leaderboard_4k.fs")
connection = database.get_connection(db)

print(connection.root().items())

print("Rank 1 player:", database.get_player_id_by_rank(connection, 1))
print("Rank 81 player:", database.get_player_id_by_rank(connection, 81))
print("Rank 10000 player:", database.get_player_id_by_rank(connection, 10000))

connection.close()
db.close()
