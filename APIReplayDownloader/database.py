from ZODB import FileStorage, DB
import transaction
import os


def open_db(main_file_name: str) -> DB:
    # if os.path.exists(main_file_name):
    #     print("Its alive")
    storage = FileStorage.FileStorage('db/testdb.fs')
    db = DB(storage)
    return db

def get_connection(db: DB):
    return db.open()


def insert_player(player_db_connection, player: dict) -> bool:
    player_id = None
    try:
        player_id = player["info"]["id"]
    except Exception as e:
        print("[ERROR]", e)
    
    if player_id != None:
        root = player_db_connection.root()

        if not player_id in root.keys(): 
            root[player_id] = player
        else:
            return False

        transaction.commit()

    return player_id != None


def update_player(player_db_connection, player: dict) -> bool:
    player_id = None
    try:
        player_id = player["info"]["id"]
    except Exception as e:
        print("[ERROR]", e)
    
    if player_id != None:
        root = player_db_connection.root()

        if player_id in root.keys(): 
            root[player_id] = player
        else:
            return False

        transaction.commit()

    return player_id != None


def insert_leaderboard_entry(leaderboard_db_connection, entry: dict) -> bool:
    player_rank = None
    try:
        player_rank = entry["stats"]["rank"]
    except Exception as e:
        print("[ERROR]", e)
    
    if player_rank != None:
        root = leaderboard_db_connection.root()

        if not player_rank in root.keys(): 
            root[player_rank] = entry
        else:
            return False

        transaction.commit()

    return player_rank != None


def update_leaderboard_entry(leaderboard_db_connection, entry: dict) -> bool:
    player_rank = None
    try:
        player_rank = entry["stats"]["rank"]
    except Exception as e:
        print("[ERROR]", e)
    
    if player_rank != None:
        root = leaderboard_db_connection.root()

        if player_rank in root.keys(): 
            root[player_rank] = entry
        else:
            return False

        transaction.commit()

    return player_rank != None