import requests
import json
import time
import os


def main():
    userids = []
    userreplaydict = {}

    user = requests.get("https://api.quavergame.com/v1/users/full/3312")

    jsonuser = json.loads(user.text)

    if jsonuser["status"] == 200:
        userids.append(jsonuser["user"]["info"]["id"])

    for id in userids:
        top50scores = requests.get(f"https://api.quavergame.com/v1/users/scores/best?id={id}&mode=1")
        jsonscores = json.loads(top50scores.text)
        if jsonscores["status"] == 200:
            replayids = []
            for score in jsonscores["scores"]:
                replayids.append(score["id"])
            userreplaydict[str(id)] = replayids

    for user in userreplaydict:
        if not os.path.exists(f"./replays/{user}"):
            os.mkdir(f"./replays/{user}")
        replayid = userreplaydict[user][0]
        replayfile = requests.get(f"https://api.quavergame.com/d/web/replay/{replayid}")

        open(f"./replays/{user}/{replayid}.qr", "wb").write(replayfile.content)


if __name__ == "__main__":
    main()
