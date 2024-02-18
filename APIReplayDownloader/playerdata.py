from requests import get
from json import loads
from time import sleep


def get_leaderboard_by_page(page: int, keymode=2) -> list:  # keymode=1 is 4k, keymode=2 is 7k (default)
    top_page = get(f"https://api.quavergame.com/v1/leaderboard?mode={keymode}&page={page}")

    json_top_page = loads(top_page.text)

    if json_top_page["status"] == 200:
        return json_top_page["users"]
    else:
        return []


def get_user_by_id(user_id: int, keymode=2) -> dict:  # keymode=1 is 4k, keymode=2 is 7k (default)
    user = get(f"https://api.quavergame.com/v1/users/full/{user_id}")

    json_user = loads(user.text)

    if json_user["status"] == 200:
        return json_user["user"]
    else:
        return {}


def get_top_scores_by_user(user_id: int, keymode=2) -> list:  # keymode=1 is 4k, keymode=2 is 7k (default)
    top_scores = get(f"https://api.quavergame.com/v1/users/scores/best?id={user_id}&mode={keymode}")

    json_top_scores = loads(top_scores.text)

    if json_top_scores["status"] == 200:
        return json_top_scores["scores"]
    else:
        return []


def download_replay(replay_id: int):
    replay = get(f"https://api.quavergame.com/d/web/replay/{replay_id}")

    return replay if replay.content is not None else None  # no idea what happens when dl fails so i'll just return none


def test():
    lb = []
    for i in range(0, 2):
        lb += get_leaderboard_by_page(i)
        sleep(1)

    for user_entry in lb:
        print(user_entry)


test()
