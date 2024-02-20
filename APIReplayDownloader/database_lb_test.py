import database

db = database.open_db("db/players.fs")
connection = database.get_connection(db)

player = database.get_player(connection, 175369)
print(player)

connection.close()
db.close()