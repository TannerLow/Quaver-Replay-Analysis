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
            transaction.commit()
        else:
            return False

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
            transaction.commit()
        else:
            return False

    return player_id != None


def get_player(player_db_connection, player_id: int) -> dict:    
    if player_id != None:
        root = player_db_connection.root()

        if player_id in root.keys():
            return root[player_id]

    return dict()


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
            transaction.commit()
        else:
            return False

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
            transaction.commit()
        else:
            return False

    return player_rank != None


def get_leaderboard_entry(leaderboard_db_connection, rank: int) -> dict:    
    if rank != None:
        root = leaderbaord_db_connection.root()

        if rank in root.keys():
            return root[rank]

    return dict()


def get_player_id_by_rank(leaderboard_db_connection, rank: int) -> int:    
    if rank != None:
        root = leaderboard_db_connection.root()

        if rank in root.keys():
            return root[rank]["id"]

    return -1