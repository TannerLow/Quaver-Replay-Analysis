from requests import get, exceptions
from json import loads


def get_ranked_mapset_ids():
    response = get("https://api.quavergame.com/v1/mapsets/ranked")

    json_response = loads(response.text)

    if json_response["status"] == 200:
        return json_response["mapsets"]
    else:
        return []


def get_mapset(mapset_id):
    response = get(f"https://api.quavergame.com/v1/mapsets/{mapset_id}")

    json_response = loads(response.text)

    if json_response["status"] == 200:
        return json_response["mapset"]
    else:
        return []


def get_map_file(map_id):
    try:
        response = get(f"https://api.quavergame.com/d/web/map/{map_id}")
        return response.content
    except exceptions.RequestException as e:  # This is the correct syntax
        print("[WARN] Unable to obtain map with ID:", map_id, "| skipping...")

    return None