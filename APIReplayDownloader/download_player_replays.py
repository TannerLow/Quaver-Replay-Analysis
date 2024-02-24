import database
from playerdata import download_replay
import os


# def download_replays():
# scores_db = database.open_db("db/scores.fs")
# scores_connection = database.get_connection(scores_db)
#
# player_db = database.open_db("db/players.fs")
# scores_connection = database.get_connection(player_db)
#
# print("Downloading ALL replays for every score in database")
#
# root = scores_connection.root()
# player_root = scores_connection.root()
#
# for id in root:
#     username = player_root[id]['info']['username']
#     scores = database.get_scores_by_id(scores_connection, id)
#
#     if not scores:
#         print(f"{username} (id {id}) has no scores, skipping...")
#         continue
#
#     print(f"Getting scores for {username} (id {id})")
#
#     user_replay_directory = f"./replays/{id}"
#     if not os.path.exists(user_replay_directory):
#         os.mkdir(user_replay_directory)
#
#     for score in scores:  # for every score that a player has in the database
#         replay_id = score["id"]
#
#         replay_file_name = f"{replay_id}.qr"
#
#         # if replay file already exists, skip it
#         if os.path.exists(f"{user_replay_directory}/{replay_file_name}"):
#             print(f"Replay (id {replay_id}) already exists, skipping...")
#             continue
#
#         # try to download the replay
#         replay = download_replay(replay_id, 2)  # 2-second sleep time
#
#         if replay:
#             replay_file = open(f"{user_replay_directory}/{replay_file_name}", "wb")
#
#             print(f"Writing {replay_file_name} to {user_replay_directory}")
#             replay_file.write(replay)
#         else:
#             continue
#
#     print(f"All scores for {username} (id {id}) downloaded.")
#
# print("Finished!")


def download_replays(scores, player_id):
    for score in scores:
        map_id = score["map"]["id"]
        keymode = "4k" if score["mode"] == 1 else "7k"
        replay_id = score["id"]

        replay = download_replay(replay_id)  # sleeps 1 second

        if replay:
            map_directory = f"./replays/{keymode}/{map_id}"
            if not os.path.exists(map_directory):
                os.mkdir(map_directory)
            open(f"{map_directory}/{player_id}_{replay_id}.qr", "wb").write(replay)
        else:
            continue


def download_replays_by_rank(lb_connection, scores_connection, rank):
    player_id = database.get_player_id_by_rank(lb_connection, rank)

    scores = database.get_scores_by_id(scores_connection, player_id)

    if scores:
        download_replays(scores, player_id)


def download_replays_by_rank_range(lb_connection, scores_connection, rank_min, rank_max):
    for rank in range(rank_min, rank_max + 1):
        player_id = database.get_player_id_by_rank(lb_connection, rank)

        scores = database.get_scores_by_id(scores_connection, player_id)

        if scores:
            download_replays(scores, player_id)


def download_replays_by_id(scores_connection, player_id):
    scores = database.get_scores_by_id(scores_connection, player_id)

    if scores:
        download_replays(scores, player_id)


# if __name__ == "__main__":
#     download_replays()
#     