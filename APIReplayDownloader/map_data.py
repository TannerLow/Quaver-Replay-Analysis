import quaver_api
import time
import os
import database
import transaction


def gather_ranked_mapsets():
    db = database.open_db("db/ranked_mapsets.fs")
    connection = database.get_connection(db)

    all_ranked_mapset_ids = quaver_api.get_ranked_mapset_ids()

    cooldown = 1
    total = len(all_ranked_mapset_ids)
    if total != 0:
        print(f"Acquiring {total} ranked mapsets.")

        # for each mapset_id get the mapset and insert into database
        for index, mapset_id in enumerate(all_ranked_mapset_ids):
            if index % 50 == 0:
                print(f"Progress: {index}/{total}")
                print("Packing database...")
                connection, db = database.pack_db(connection, db)

            root = connection.root()
            mapset = None
            if not mapset_id in root.keys():
                mapset = quaver_api.get_mapset(mapset_id)

            if mapset != None:
                transaction.begin()
                status = database.insert_mapset(connection, mapset)
                print(f"Getting mapset {mapset_id}: {status}")
                if status == True:
                    transaction.commit()
                else:
                    transaction.abort()
            
                time.sleep(cooldown)
        
        print("Done gathering mapsets")

    connection, db = database.pack_db(connection, db)
    connection.close()
    db.close()



def gather_maps(map_ids):
    cooldown = 3
    map_directory = "maps"

    total = len(map_ids)
    if total != 0:
        print(f"Acquiring {total} map files.")

        if not os.path.exists(map_directory):
            os.makedirs(map_directory)

        for index, map_id in enumerate(map_ids):
            if index % 50 == 0:
                print(f"Progress: {index}/{total}")

            filename = str(map_id) + ".qua"
            filename = os.path.join(map_directory, filename)
            
            map_content = None
            if not os.path.exists(filename):
                map_content = quaver_api.get_map_file(map_id)

            if map_content != None:
                with open(filename, "wb") as file:
                    file.write(map_content)
                    print("Map retrieved:", map_id)
                
                time.sleep(cooldown)
        
        print("Done gathering maps")
                



if __name__ == "__main__":
    gather_ranked_mapsets()

    db = database.open_db("db/ranked_mapsets.fs")
    connection = database.get_connection(db)

    map_ids = set()
    root = connection.root()
    for key in root.keys():
        for map_obj in root[key]["maps"]:
            map_ids.add(map_obj["id"])

    connection.close()
    db.close()

    gather_maps(map_ids)