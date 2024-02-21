import database
import transaction
from playerdata import get_user_by_id
from time import sleep

# 4k section

leaderboard_4k_db = database.open_db("db/leaderboard_4k.fs")
leaderboard_4k_connection = database.get_connection(leaderboard_4k_db)

player_db = database.open_db("db/players.fs")
player_connection = database.get_connection(player_db)

print("Pre-packing database...")

player_connection, player_db = database.pack_db(player_connection, player_db)

print("Adding players from 4k leaderboard to database...")

num_profiles_added = 0
root = leaderboard_4k_connection.root()
num_players = len(root.keys())

for rank in root.keys():  # for all ranks on the 4k leaderboard
    player_id = root[rank]["id"]

    if num_profiles_added == 0:
        transaction.begin()

    if database.get_player(player_connection, player_id) != {}:
        print(f"Player (id {player_id}) already in database. Skipping...")
        continue

    player_profile = get_user_by_id(player_id, 1)  # 1 means 4k
    sleep(1)

    if player_profile:
        print(f"Adding {player_profile['info']['username']} (id {player_id}) to database:",
              database.insert_player(player_connection, player_profile))

        num_profiles_added += 1

        if num_profiles_added % 25 == 0:
            transaction.commit()
            transaction.begin()

        if num_profiles_added % 250 == 0:
            print(f"Packing db... {num_profiles_added / num_players}% complete")
            player_connection, player_db = database.pack_db(player_connection, player_db)

transaction.commit()

print("Final pack...")
player_connection, player_db = database.pack_db(player_connection, player_db)
print("Done!")

leaderboard_4k_connection.close()
leaderboard_4k_db.close()

# 7k section

leaderboard_7k_db = database.open_db("db/testdb.fs")
leaderboard_7k_connection = database.get_connection(leaderboard_7k_db)

print("Adding players from 7k leaderboard to database...")

num_profiles_added = 0
root = leaderboard_7k_connection.root()
num_players = len(root.keys())

for rank in root.keys():  # for all ranks on the 4k leaderboard
    player_id = root[rank]["id"]

    if num_profiles_added == 0:
        transaction.begin()

    if database.get_player(player_connection, player_id) != {}:
        print(f"Player (id {player_id}) already in database. Skipping...")
        continue

    player_profile = get_user_by_id(player_id)
    sleep(1)

    if player_profile:
        print(f"Adding {player_profile['info']['username']} (id {player_id}) to database:",
              database.insert_player(player_connection, player_profile))

        num_profiles_added += 1

        if num_profiles_added % 25 == 0:
            transaction.commit()
            transaction.begin()

        if num_profiles_added % 250 == 0:
            print(f"Packing db... {num_profiles_added / num_players}% complete")
            player_connection, player_db = database.pack_db(player_connection, player_db)


transaction.commit()

print("Final pack...")
player_connection, player_db = database.pack_db(player_connection, player_db)
print("Done!")

leaderboard_7k_connection.close()
leaderboard_7k_db.close()

player_connection.close()
player_db.close()
