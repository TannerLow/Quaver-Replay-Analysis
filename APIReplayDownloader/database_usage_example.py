import database

db = database.open_db("db/testdb.fs")
connection = database.get_connection(db)

print(connection.root().items())

sample_player = {
    "info": {
        "id": 1,
        "steam_id": "76561198162013525",
        "username": "Swan",
        "time_registered": "2018-12-16T20:27:20.447Z",
        "allowed": 1,
        "privileges": 8191,
        "usergroups": 507,
        "mute_endtime": "2018-12-20T20:36:20.000Z",
        "latest_activity": "2021-01-18T00:52:38.523Z",
        "country": "US",
        "avatar_url": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fa/fa444c36d0a5e016f3c4d664cf832be4a7e3d4ad_full.jpg",
        "userpage": "[center][img]https://i.imgur.com/rk6hg8Q.png[/img]\r\n\r\n\r\nCreator & Lead Developer of [b]Quaver.[/b]\r\n\r\nFollow us on [url=https://twitter.com/QuaverGame]Twitter[/url], and join the [url=https://discord.gg/nJa8VFr]Discord[/url] for updates.\r\n\r\n\r\n[b]Contact Links[/b]\r\n\r\n[url=mailto:me@swan.moe]Email[/url] | [url=https://github.com/Swan]GitHub[/url] | [url=https://twitter.com/Swanuh]Twitter[/url] | [url=https://steamcommunity.com/profiles/76561198162013525]Steam[/url] \r\n[/center]",
        "information": {
            "discord": "Swan#1337",
            "twitter": "Swanuh",
            "twitch": "Swanuh",
            "youtube": "https://www.youtube.com/channel/UCGWaxO5T6NzCo3G1jIIKlMA"
        },
        "online": False
    },
    "profile_badges": [
        {
            "id": 3,
            "name": "Donator",
            "description": "Generously supported Quaver by making a donation"
        }
    ],
    "activity_feed": [
        {
            "id": 357416,
            "type": 8,
            "timestamp": "2020-12-19T18:31:13.921Z",
            "map": {
                "id": -1,
                "name": "Donated to Quaver!"
            }
        }
    ],
    "keys4": {
        "globalRank": 175,
        "countryRank": 41,
        "multiplayerWinRank": 139,
        "stats": {
            "user_id": 1,
            "total_score": 1286461145,
            "ranked_score": 654468148,
            "overall_accuracy": 98.39068437173286,
            "overall_performance_rating": 722.7637109351122,
            "play_count": 1613,
            "fail_count": 295,
            "max_combo": 3588,
            "replays_watched": 0,
            "total_marv": 5405614,
            "total_perf": 2161770,
            "total_great": 279108,
            "total_good": 40107,
            "total_okay": 14946,
            "total_miss": 48238,
            "total_pauses": 0,
            "multiplayer_wins": 140,
            "multiplayer_losses": 351,
            "multiplayer_ties": 14
        }
    },
    "keys7": {
        "globalRank": 1134,
        "countryRank": 185,
        "multiplayerWinRank": 97970,
        "stats": {
            "user_id": 1,
            "total_score": 110624489,
            "ranked_score": 99116539,
            "overall_accuracy": 93.51298667660535,
            "overall_performance_rating": 125.24914600037367,
            "play_count": 155,
            "fail_count": 13,
            "max_combo": 625,
            "replays_watched": 0,
            "total_marv": 92262,
            "total_perf": 52494,
            "total_great": 8826,
            "total_good": 1920,
            "total_okay": 751,
            "total_miss": 4035,
            "total_pauses": 0,
            "multiplayer_wins": 0,
            "multiplayer_losses": 2,
            "multiplayer_ties": 0
        }
    }
}

sample_entry = {
    "id": 383,
    "steam_id": "76561198114893591",
    "username": "yahweh",
    "country": "US",
    "allowed": 1,
    "privileges": 33,
    "usergroups": 33,
    "avatar_url": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/dc/dcb7ff72103ebdd699f0087e752370df49caddae_full.jpg",
    "time_registered": "2019-03-04T21:15:19.418Z",
    "latest_activity": "2021-01-19T22:01:21.794Z",
    "stats": {
        "rank": 1,
        "ranked_score": 1310753785,
        "overall_accuracy": 97.65194001521708,
        "overall_performance_rating": 872.3279130058347,
        "play_count": 2795,
        "max_combo": 4123
    }
}

print("Attempt to add player database:", database.insert_player(connection, sample_player))
print("Attempt to add player database:", database.update_player(connection, sample_player))

print("Attempt to add player database:", database.insert_leaderboard_entry(connection, sample_entry))
print("Attempt to add player database:", database.update_leaderboard_entry(connection, sample_entry))

connection.close()
db.close()