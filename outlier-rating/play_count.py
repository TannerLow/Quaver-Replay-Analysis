import matplotlib.pyplot as plt
import numpy as np
import bisect
import copy


def get_play_counts(leaderboard_connection, play_count_hard_cap=30000):
    indexes = dict()
    play_counts = []

    root = leaderboard_connection.root()
    for rank in root.keys():
        leaderboard_entry = root[rank]
        play_count = leaderboard_entry["stats"]["play_count"]
        if play_count < play_count_hard_cap:
            play_counts.append(play_count)
            indexes[rank] = len(play_counts) - 1
    
    return play_counts, indexes


def plot_play_count_vs_rank(play_counts, indexes, mode):
    mode_string = "4k"
    if mode == 2:
        mode_string = "7k"

    max_rank = max(indexes.keys())

    sorted_ranks = []
    sorted_counts = []
    for rank in range(max_rank):
        if rank in indexes.keys():
            sorted_counts.append(play_counts[indexes[rank]])
            sorted_ranks.append(rank)

    plt.clf()
    plt.plot(sorted_ranks, sorted_counts)
    plt.xlim(xmax=max_rank, xmin=0)
    plt.ylim(ymin=0)
    plt.xlabel("Rank")
    plt.ylabel("Play Count")
    plt.title("Play Count vs. Rank")
    plt.savefig(f"results/play_count_vs_rank_{mode_string}.png")


def create_groups(play_counts, indexes, group_count):
    max_rank = max(indexes.keys())
    group_size = max_rank // group_count

    groups = []
    group_ranges = dict()
    for rank in range(max_rank):
        if rank in indexes.keys():
            group_index = rank // group_size
            if len(groups) <= group_index:
                groups.append(list())
                group_ranges[group_index] = {"min": rank, "max": rank}
            groups[group_index].append(play_counts[indexes[rank]])
            group_ranges[group_index]["max"] = rank
    
    return groups, group_ranges


def plot_play_count_histograms(play_counts, indexes, group_count, mode):
    mode_string = "4k"
    if mode == 2:
        mode_string = "7k"

    groups, group_ranges = create_groups(play_counts, indexes, group_count)
    
    print(group_ranges)
    
    for group_index in group_ranges.keys():
        bin_size = 100
        plt.clf()
        plt.hist(groups[group_index], max(groups[group_index]) // bin_size)
        min_rank = group_ranges[group_index]["min"]
        max_rank = group_ranges[group_index]["max"]
        plt.savefig(f"results/histogram_{mode_string}_{min_rank}_{max_rank}.png")
        print(f"{min_rank}_{max_rank}: mean: {np.mean(groups[group_index])}, std: {np.std(groups[group_index])}")


def calculate_percentile_in_group(rank, play_count, groups, group_ranges):
    for group_index, group_range in group_ranges.items():
        if group_range["min"] <= rank <= group_range["max"]:
            play_counts = groups[group_index].copy()
            play_counts.sort()
            # get index where value would be inserted into list of sorted play counts
            index = bisect.bisect_left(play_counts, play_count)
            return index / len(play_counts)

            
