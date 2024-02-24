from requests import get, exceptions
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
    try:
        user = get(f"https://api.quavergame.com/v1/users/full/{user_id}")
    except exceptions.Timeout:
        print(f"Timed out, skipping id ({user_id})")
        return {}

    json_user = loads(user.text)

    if json_user["status"] == 200:
        return json_user["user"]
    else:
        return {}


def get_top_scores_by_user(user_id: int, keymode=2, num_pages=1) -> list:  # keymode=1 is 4k, keymode=2 is 7k (default)
    scores = []
    for page in range(num_pages):
        try:
            top_scores = get(f"https://api.quavergame.com/v1/users/scores/best?id={user_id}&mode={keymode}&page={page}", 5)
            sleep(1)
        except exceptions.Timeout:
            print(f"Timed out, skipping page {page} of {num_pages} for id ({user_id})")
            continue

        json_scores = loads(top_scores.text)

        if json_scores["status"] == 200:
            scores.extend(json_scores["scores"])

        if json_scores["status"] == 404:
            print(f"User does not have enough top scores set. Stopping...")
            return scores

    return scores


def download_replay(replay_id: int, sleep_time=1):
    try:
        replay = get(f"https://api.quavergame.com/d/web/replay/{replay_id}", timeout=5)
        sleep(sleep_time)
    except exceptions.Timeout:
        print(f"Getting replay id ({replay_id}) timed out, skipping...")
        return None

    return replay.content


def test():
    lb = []
    for i in range(0, 2):
        lb += get_leaderboard_by_page(i)
        sleep(1)

    for user_entry in lb:
        print(user_entry)


# test()
