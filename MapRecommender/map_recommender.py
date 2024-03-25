import database
from random import choice


def recommend_maps(player_id: int, mode: int, num_maps=1, for_qr=True, include_new=True):
    if mode == 1:
        lb_db = database.open_db("../APIReplayDownloader/db/leaderboard_4k.fs")
        lb_connection = database.get_connection(lb_db)

        scores_db = database.open_db("../APIReplayDownloader/db/scores_4k.fs")
        scores_connection = database.get_connection(scores_db)
    elif mode == 2:
        lb_db = database.open_db("../APIReplayDownloader/db/testdb.fs")
        lb_connection = database.get_connection(lb_db)

        scores_db = database.open_db("../APIReplayDownloader/db/scores_7k.fs")
        scores_connection = database.get_connection(scores_db)
    else:
        print("invalid mode")
        return

    player_scores = scores_db.get_scores_by_id(scores_connection, player_id)
    player_score_ids = []

    for score in player_scores:
        player_score_ids.append(score["map"]["id"])

    ranked_maps_db = database.open_db("../APIReplayDownloader/db/ranked_mapsets.fs")
    ranked_maps_connection = database.get_connection(ranked_maps_db)

    top_50_average = 0
    for score in player_scores[:50]:
        top_50_average += score["performance_rating"]
    top_50_average /= 50

    if for_qr:  # 5% more than player's avg. top 50 (better metric than avg. top 20 + 3)
        qr_range = [top_50_average * 1.05, player_scores[0]["performance_rating"] + 1]
    else:
        qr_range = [player_scores[49]["performance_rating"], player_scores[0]["performance_rating"]]

    possible_maps = []

    root = ranked_maps_connection.root()
    for map_id in root.keys():
        if qr_range[0] <= root[map_id]["difficulty_rating"] <= qr_range[1]:
            if include_new and map_id in player_score_ids:
                continue
            else:
                possible_maps.append(map_id)

    maps_to_recommend = []

    for _ in range(num_maps):
        map = choice(possible_maps)
        if map not in maps_to_recommend:
            maps_to_recommend.append(map)

