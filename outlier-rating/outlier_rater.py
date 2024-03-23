import database
import os
import shutil
import play_count


# This file should contain only driver code and helper functions.
# Data collection should be separated


if os.path.exists("results"):
    shutil.rmtree("results")
os.mkdir("results")

group_count = 10

# Process 4k players play counts
mode = 1
leaderboard_db = database.open_db("db/leaderboard_4k.fs")
leaderboard_connection = database.get_connection(leaderboard_db)

play_counts, play_count_indexes = play_count.get_play_counts(leaderboard_connection)
play_count.plot_play_count_vs_rank(play_counts, play_count_indexes, mode)
play_count.plot_play_count_histograms(play_counts, play_count_indexes, group_count, mode)

leaderboard_connection.close()
leaderboard_db.close()

# Process 7k players play counts
mode = 2
leaderboard_db = database.open_db("db/leaderboard_7k.fs")
leaderboard_connection = database.get_connection(leaderboard_db)

#print(f"Play Counts: {play_counts}")
#print(f"indexes: {play_count_indexes}")

play_counts, play_count_indexes = play_count.get_play_counts(leaderboard_connection)
play_count.plot_play_count_vs_rank(play_counts, play_count_indexes, mode)
play_count.plot_play_count_histograms(play_counts, play_count_indexes, group_count, mode)

leaderboard_connection.close()
leaderboard_db.close()

groups, group_ranges = play_count.create_groups(play_counts, play_count_indexes, group_count)
print(play_count.calculate_percentile_in_group(1, 700, groups, group_ranges))