import database
import transaction
from playerdata import get_top_scores_by_user


def get_scores(num_pages=1):
    player_4k_db = database.open_db("db/leaderboard_4k.fs")
    player_4k_connection = database.get_connection(player_4k_db)

    player_7k_db = database.open_db("db/testdb.fs")
    player_7k_connection = database.get_connection(player_7k_db)

    scores_4k_db = database.open_db("db/scores_4k.fs")
    scores_4k_connection = database.get_connection(scores_4k_db)

    scores_7k_db = database.open_db("db/scores_7k.fs")
    scores_7k_connection = database.get_connection(scores_7k_db)

    print("Pre-packing databases...")

    scores_4k_connection, scores_4k_db = database.pack_db(scores_4k_connection, scores_4k_db)
    scores_7k_connection, scores_7k_db = database.pack_db(scores_7k_connection, scores_7k_db)

    print("Getting scores from all players in 4k database...")

    root_4k = player_4k_connection.root()

    num_profiles_added = 0
    for rank in root_4k.keys():  # for every player in our player database
        if num_profiles_added == 0:
            transaction.begin()

        player_id = database.get_player_id_by_rank(player_4k_connection, rank)

        if len(database.get_scores_by_id(scores_4k_connection, player_id)) == 50 * num_pages:
            # if player already has the same amount of scores as we are requesting, skip
            print(f"User id ({player_id}) already has {50*num_pages} scores in database, skipping...")
            continue

        scores = get_top_scores_by_user(player_id, 1, num_pages)  # sleep(1) is built-in to helper function

        if scores:  # if we got scores from the api, add them to the user in the database
            print(f"Adding scores to id ({player_id}) in database:", database.insert_scores(scores_4k_connection, player_id, scores))

        num_profiles_added += 1

        # commit every 25 users
        if num_profiles_added % 25 == 0:
            print("Committing...")
            transaction.commit()
            transaction.begin()

        # pack every 200 users
        if num_profiles_added % 200 == 0:
            print("Packing database...")
            scores_4k_connection, scores_4k_db = database.pack_db(scores_4k_connection, scores_4k_db)

    transaction.commit()

    print("Final pack...")

    scores_4k_connection, scores_4k_db = database.pack_db(scores_4k_connection, scores_4k_db)

    print("Done!")

    scores_4k_connection.close()
    scores_4k_db.close()

    player_4k_connection.close()
    player_4k_db.close()

    print("Getting all scores from players in 7k database")

    root_7k = player_7k_connection.root()

    num_profiles_added = 0
    for rank in root_7k.keys():  # for every player in our player database
        if num_profiles_added == 0:
            transaction.begin()

        player_id = database.get_player_id_by_rank(player_7k_connection, rank)

        if len(database.get_scores_by_id(scores_7k_connection, player_id)) == 50 * num_pages:
            # if player already has the same amount of scores as we are requesting, skip
            print(f"User id ({player_id}) already has {50 * num_pages} scores in database, skipping...")
            continue

        scores = get_top_scores_by_user(player_id, num_pages=num_pages)  # sleep(1) is built-in to helper function

        if scores:  # if we got scores from the api, add them to the user in the database
            print(f"Adding scores to id ({player_id}) in database:",
                  database.insert_scores(scores_7k_connection, player_id, scores))

        num_profiles_added += 1

        # commit every 25 users
        if num_profiles_added % 25 == 0:
            print("Committing...")
            transaction.commit()
            transaction.begin()

        # pack every 200 users
        if num_profiles_added % 200 == 0:
            print("Packing database...")
            scores_7k_connection, scores_7k_db = database.pack_db(scores_7k_connection, scores_7k_db)

    transaction.commit()

    print("Final pack...")

    scores_7k_connection, scores_7k_db = database.pack_db(scores_7k_connection, scores_7k_db)

    print("Done!")

    scores_7k_connection.close()
    scores_7k_db.close()

    player_7k_connection.close()
    player_7k_db.close()


if __name__ == "__main__":
    get_scores()  # takes number of pages as parameter, 1 is default
