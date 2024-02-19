import quaver_api
import time
import os


cooldown = 3
map_directory = "maps"

def gather_maps():
    all_ranked_map_ids = quaver_api.get_ranked_map_ids()

    total = len(all_ranked_map_ids)
    if total != 0:
        print(f"Acquiring {total} ranked maps.")

        if not os.path.exists(map_directory):
            os.makedirs(map_directory)

        for index, map_id in enumerate(all_ranked_map_ids):
            if index % 50 == 0:
                print(f"Progress: {index}/{total}")
            map_content = quaver_api.get_map_file(map_id)

            if map_content != None:
                filename = str(map_id) + ".qua"
                filename = os.path.join(map_directory, filename)
                with open(filename, "wb") as file:
                    file.write(map_content)

            time.sleep(cooldown)
        
        print("Done gathering maps")
                


if __name__ == "__main__":
    gather_maps()