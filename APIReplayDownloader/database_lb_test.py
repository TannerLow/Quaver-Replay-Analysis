import database

db = database.open_db("db/testdb.fs")
connection = database.get_connection(db)

id = database.get_player_id_by_rank(connection, 90)
print(id)

connection.close()
db.close()