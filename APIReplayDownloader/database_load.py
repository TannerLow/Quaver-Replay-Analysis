import database
import transaction
from playerdata import get_user_by_id
from time import sleep

leaderboard_4k_db = database.open_db("db/leaderboard_4k.fs")
leaderboard_4k_connection = database.get_connection(leaderboard_4k_db)

player_db = database.open_db("db/players.fs")
player_connection = database.get_connection(player_db)

print("Adding players from 4k leaderboard to database...")

num = 0
for i in range(1, 50):  # for all ranks in the 4k leaderboard db
    player_id = database.get_player_id_by_rank(leaderboard_4k_connection, i)

    if player_id != -1:
        if database.get_player(player_connection, player_id) != {}:
            print(f"Player (id {player_id}) already in database. Skipping...")
            continue
        player_profile = get_user_by_id(player_id, 1)  # 1 means 4k
        if player_profile:
            transaction.begin()
            print(f"Adding {player_profile['info']['username']} (id {player_id}) to database:",
                  database.insert_player(player_connection, player_profile))
            transaction.commit()
            num += 1
            if num % 500 == 0:
                print(f"Packing db... {num / 10050}% complete")
                player_connection, player_db = database.pack_db(player_connection, player_db)
        sleep(1)

print("Final pack...")
player_connection, player_db = database.pack_db(player_connection, player_db)
print("Done!")

leaderboard_4k_connection.close()
leaderboard_4k_db.close()

leaderboard_7k_db = database.open_db("db/testdb.fs")
leaderboard_7k_connection = database.get_connection(leaderboard_7k_db)

print("Adding players from 7k leaderboard to database...")

num = 0
for i in range(50, 100):  # for all ranks in the 7k leaderboard db
    player_id = database.get_player_id_by_rank(leaderboard_7k_connection, i)

    if player_id != -1:
        if database.get_player(player_connection, player_id) != {}:
            print(f"Player (id {player_id}) already in database. Skipping...")
            continue
        player_profile = get_user_by_id(player_id)
        if player_profile:
            transaction.begin()
            print(f"Adding {player_profile['info']['username']} (id {player_id}) to database:",
                  database.insert_player(player_connection, player_profile))
            transaction.commit()
            num += 1
            if num % 500 == 0:
                print(f"Packing db... {num / 3550}% complete")
                player_connection, player_db = database.pack_db(player_connection, player_db)
        sleep(1)

print("Final pack...")
player_connection, player_db = database.pack_db(player_connection, player_db)
print("Done!")

leaderboard_7k_connection.close()
leaderboard_7k_db.close()

player_connection.close()
player_db.close()
