import database
from playerdata import download_replay
import os


def download_all_replays(lb_connection, scores_connection):
    root = lb_connection.root()

    for rank in root.keys():
        print(f"Downloading replays for {root[rank]['username']} (id {root[rank]['id']})")
        download_replays_by_rank(lb_connection, scores_connection, rank)


def download_replays(scores, player_id):
    for score in scores:
        map_id = score["map"]["id"]
        keymode = "4k" if score["mode"] == 1 else "7k"
        replay_id = score["id"]

        map_directory = f"./replays/{keymode}/{map_id}"
        filename = f"{player_id}_{replay_id}.qr"

        if os.path.exists(f"{map_directory}/{filename}"):
            print(f"Replay id ({replay_id}) already downloaded, skipping...")
            continue

        replay = download_replay(replay_id)  # sleeps 1 second

        if replay:
            if not os.path.exists(map_directory):
                os.mkdir(map_directory)
            open(f"{map_directory}/{filename}", "wb").write(replay)
            print(f"Downloaded replay id ({replay_id}) for {keymode} map {score['map']['title']}")
        else:
            continue


def download_replays_by_rank(lb_connection, scores_connection, rank):
    player_id = database.get_player_id_by_rank(lb_connection, rank)

    scores = database.get_scores_by_id(scores_connection, player_id)

    if scores:
        download_replays(scores, player_id)


def download_replays_by_rank_range(lb_connection, scores_connection, rank_min, rank_max):
    root = lb_connection.root()

    for rank in range(rank_min, rank_max + 1):
        player_id = database.get_player_id_by_rank(lb_connection, rank)

        scores = database.get_scores_by_id(scores_connection, player_id)

        print(f"Downloading replays for {root[rank]['username']} (id {player_id})")

        if scores:
            download_replays(scores, player_id)


def download_replays_by_id(lb_connection, scores_connection, player_id):
    root = lb_connection.root()

    scores = database.get_scores_by_id(scores_connection, player_id)

    print(f"Downloading replays for {root[rank]['username']} (id {player_id})")

    if scores:
        download_replays(scores, player_id)


if __name__ == "__main__":
    player_4k_db = database.open_db("db/leaderboard_4k.fs")
    player_4k_connection = database.get_connection(player_4k_db)

    scores_4k_db = database.open_db("db/scores_4k.fs")
    scores_4k_connection = database.get_connection(scores_4k_db)

    download_all_replays(player_4k_connection, scores_4k_connection)

    scores_4k_connection.close()
    scores_4k_db.close()

    player_4k_connection.close()
    player_4k_db.close()

    player_7k_db = database.open_db("db/testdb.fs")
    player_7k_connection = database.get_connection(player_7k_db)

    scores_7k_db = database.open_db("db/scores_7k.fs")
    scores_7k_connection = database.get_connection(scores_7k_db)

    download_all_replays(player_7k_connection, scores_7k_connection)

    scores_7k_connection.close()
    scores_7k_db.close()

    player_7k_connection.close()
    player_7k_db.close()
