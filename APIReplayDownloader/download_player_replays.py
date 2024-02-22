import database
from playerdata import download_replay
import os


def download_replays():
    scores_db = database.open_db("db/scores.fs")
    scores_connection = database.get_connection(scores_db)

    player_db = database.open_db("db/players.fs")
    scores_connection = database.get_connection(player_db)

    print("Downloading ALL replays for every score in database")

    root = scores_connection.root()
    player_root = scores_connection.root()

    for id in root:
        username = player_root[id]['info']['username']
        scores = database.get_scores_by_id(scores_connection, id)

        if not scores:
            print(f"{username} (id {id}) has no scores, skipping...")
            continue

        print(f"Getting scores for {username} (id {id})")

        user_replay_directory = f"./replays/{id}"
        if not os.path.exists(user_replay_directory):
            os.mkdir(user_replay_directory)

        for score in scores:  # for every score that a player has in the database
            replay_id = score["id"]

            replay_file_name = f"{replay_id}.qr"

            # if replay file already exists, skip it
            if os.path.exists(f"{user_replay_directory}/{replay_file_name}"):
                print(f"Replay (id {replay_id}) already exists, skipping...")
                continue

            # try to download the replay
            replay = download_replay(replay_id, 2)  # 2-second sleep time

            if replay:
                replay_file = open(f"{user_replay_directory}/{replay_file_name}", "wb")

                print(f"Writing {replay_file_name} to {user_replay_directory}")
                replay_file.write(replay)
            else:
                continue

        print(f"All scores for {username} (id {id}) downloaded.")

    print("Finished!")


if __name__ == "__main__":
    download_replays()
