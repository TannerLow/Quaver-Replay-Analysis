from ZODB import FileStorage, DB, serialize
import transaction
import os
import time


def open_db(main_file_name: str) -> DB:
    storage = FileStorage.FileStorage(main_file_name)
    db = DB(storage)
    return db


# The storage should be closed before calling pack()
def pack_db(connection, db: DB):
    # free resources
    db_file_name = db.storage.getName()
    connection.close()
    db.close()
    # pack the storage
    storage = FileStorage.FileStorage(db_file_name)
    storage.pack(time.time(), serialize.referencesf)
    storage.close()
    # reestablish database
    new_db = open_db(db_file_name)
    new_connection = get_connection(new_db)
    return new_connection, new_db


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
        else:
            return False

    return player_rank != None


def get_leaderboard_entry(leaderboard_db_connection, rank: int) -> dict:    
    if rank != None:
        root = leaderboard_db_connection.root()

        if rank in root.keys():
            return root[rank]

    return dict()


def get_player_id_by_rank(leaderboard_db_connection, rank: int) -> int:    
    if rank != None:
        root = leaderboard_db_connection.root()

        if rank in root.keys():
            return root[rank]["id"]

    return -1


def insert_mapset(mapset_db_connection, mapset: dict) -> bool:
    mapset_id = None
    try:
        mapset_id = mapset["id"]
    except Exception as e:
        print("[ERROR]", e)
    
    if mapset_id != None:
        root = mapset_db_connection.root()

        if not mapset_id in root.keys():
            root[mapset_id] = mapset
        else:
            return False

    return mapset_id != None


def update_mapset(mapset_db_connection, mapset: dict) -> bool:
    mapset_id = None
    try:
        mapset_id = mapset["id"]
    except Exception as e:
        print("[ERROR]", e)
    
    if mapset_id != None:
        root = mapset_db_connection.root()

        if mapset_id in root.keys(): 
            root[mapset_id] = mapset
        else:
            return False

    return mapset_id != None


def get_mapset(mapset_db_connection, mapset_id: int) -> dict:    
    if mapset_id != None:
        root = mapset_db_connection.root()

        if mapset_id in root.keys():
            return root[mapset_id]

    return dict()


def get_scores_by_id(score_db_connection, player_id: int) -> list:
    if player_id != None:
        root = score_db_connection.root()

        if player_id in root.keys():
            return root[player_id]

    return []