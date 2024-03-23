from playerdata import get_top_scores_by_user
import math
import numpy as np


def get_average_play_qr(user_id, num_of_plays, mode=2):
    num_of_pages = int(math.ceil(num_of_plays / 50))
    scores = get_top_scores_by_user(user_id, mode, num_of_pages)
    
    selected_plays = []
    for i in range(num_of_plays):
        selected_plays.append(scores[i]["performance_rating"])
    
    return np.mean(selected_plays)

def get_minimum_top_play_qr(user_id, num_of_plays, mode=2):
    num_of_pages = int(math.ceil(num_of_plays / 50))
    scores = get_top_scores_by_user(user_id, mode, num_of_pages)
    
    selected_plays = []
    for i in range(num_of_plays):
        selected_plays.append(scores[i]["performance_rating"])
    
    return min(selected_plays)