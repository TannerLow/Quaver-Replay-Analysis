import database
import transaction
from playerdata import get_top_scores_by_user


def get_scores(num_pages=1):
    player_db = database.open_db("db/players.fs")
    player_connection = database.get_connection(player_db)

    scores_db = database.open_db("db/scores.fs")
    scores_connection = database.get_connection(scores_db)

    print("Pre-packing database...")

    scores_connection, scores_db = database.pack_db(player_connection, player_db)

    print("Getting scores from all players in database...")

    root = player_connection.root()

    num_profiles_added = 0
    for id in root.keys():  # for every player in our player database
        if num_profiles_added == 0:
            transaction.begin()

        if len(database.get_scores_by_id(scores_connection, id)) == 50 * num_pages:
            # if player already has the same amount of scores as we are requesting, skip
            print(f"User id ({id}) already has {50*num_pages} scores in database, skipping...")
            continue

        scores = get_top_scores_by_user(id, num_pages=num_pages)  # sleep(1) is built-in to helper function

        if scores:  # if we got scores from the api, add them to the user in the database
            print(f"Adding scores to id ({id}) in database:", database.insert_scores(scores_connection, id, scores))

        num_profiles_added += 1

        # commit every 25 users
        if num_profiles_added % 25 == 0:
            print("Committing...")
            transaction.commit()
            transaction.begin()

        # pack every 200 users
        if num_profiles_added % 200 == 0:
            print("Packing database...")
            scores_connection, scores_db = database.pack_db(scores_connection, scores_db)

    transaction.commit()

    print("Final pack...")

    scores_connection, scores_db = database.pack_db(scores_connection, scores_db)

    print("Done!")

    scores_connection.close()
    scores_db.close()

    player_connection.close()
    player_db.close()


if __name__ == "__main__":
    get_scores()  # takes number of pages as parameter, 1 is default
