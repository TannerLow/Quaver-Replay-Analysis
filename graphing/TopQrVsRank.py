import matplotlib.pyplot as plt
import csv
import database
import numpy as np

np.seterr(all='raise')


# Just get scores but don't process them
def get_scores(leaderboard_connection, scores_connection, player_connection, num_of_scores):
    ranks = []
    top_n_plays_qr = []

    root = leaderboard_connection.root()
    for rank in range(len(root.keys())):
        rank = rank + 1 # ranks start at 1
        player_id = database.get_player_id_by_rank(leaderboard_connection, rank)
        player = database.get_player(player_connection, player_id)
        #print("Current player:", player["info"]["username"])
        scores = database.get_scores_by_id(scores_connection, player_id)

        qrs = []
        for i in range(num_of_scores):
            if i < len(scores):
                qrs.append(scores[i]["performance_rating"])

        if len(qrs) == 0:
            print("Idiot player profile:", player["info"]["username"])
            #print("player id:", player_id)
            #print("player:", player)
            #print("scores:", scores)
        else:
            top_n_plays_qr.append(qrs)
            ranks.append(rank)

    return ranks, top_n_plays_qr


# helper to create N near equal sized sublists from 1 big list
def split_list(lst, n):
    size = len(lst) // n
    start = 0
    sublists = []
    for _ in range(n - 1):
        end = start + size
        sublists.append(lst[start:end])
        start = end

    sublists.append(lst[start:])
    return sublists

# Get mean and std dev. of each player's scores for all players
# Group into equal size bins based on rank
# Calculate the mean and std dev. of the std dev's for each player in each bin
# If the player's standard deviation is more than 1 positive standard deviation above the mean
#   then remove them
# Aggregate bins
def remove_outliers(ranks, top_n_plays_qr):
    bin_count = 5
    player_means = []
    player_std_devs = []

    if len(ranks) != len(top_n_plays_qr):
        print("Unexpected length mismatch:", len(ranks), "vs.", len(top_n_plays_qr))
        exit(1)

    for i in range(len(top_n_plays_qr)):
        player_means.append(np.mean(top_n_plays_qr[i]))
        player_std_devs.append(np.std(top_n_plays_qr[i]))

    split_ranks = split_list(ranks, bin_count)
    split_top_n_plays_qr = split_list(top_n_plays_qr, bin_count)
    split_player_means = split_list(player_means, bin_count)
    split_player_std_devs = split_list(player_std_devs, bin_count)

    deleted_count = 0
    new_ranks = []
    new_top_n_plays_qr = []
    for bin in range(bin_count):
        std_devs = split_player_std_devs[bin]
        mean = np.mean(std_devs)
        std_dev = np.std(std_devs)
        one_std_dev_above = mean + std_dev

        indexes_to_delete = []
        for i in range(len(std_devs)):
            if std_devs[i] >= one_std_dev_above:
                indexes_to_delete.append(i)
        
        offset = 0
        for index in indexes_to_delete:
            del split_ranks[bin][index + offset]
            del split_top_n_plays_qr[bin][index + offset]
            deleted_count += 1
            offset -= 1

    print("Number of players deleted in filter process:", deleted_count)

    for sublist in split_ranks:
        new_ranks += sublist

    for sublist in split_top_n_plays_qr:
        new_top_n_plays_qr += sublist

    return new_ranks, new_top_n_plays_qr


# Assumes ranks and top_n_plays_qr are equal in size
def create_datasets(ranks, top_n_plays_qr, stride, num_of_scores):
    rank_bins = []
    average_top15_qr = []

    batch_count = len(ranks) // stride
    index = 0
    for batch in range(batch_count):
        batch_averages = []
        for i in range(stride):
            scores = top_n_plays_qr[index]
            index += 1

            sum = 0
            scores_counted = 0
            for k in range(num_of_scores):
                if k < len(scores):
                    sum += scores[k]
                    scores_counted += 1
                else:
                    break

            if scores_counted > 0:
                batch_averages.append(sum / scores_counted)

        sum = 0
        for average in batch_averages:
            sum += average

        average_top15_qr.append(sum / len(batch_averages))
        rank_bins.append(ranks[index])

    return rank_bins, average_top15_qr


def generate_trendline(plt, x, y, degree, color):
    # Fit a polynomial of degree 1 (linear fit) to your data
    coefficients = np.polyfit(x, y, degree)

    # Create a polynomial function using the coefficients
    trendline = np.poly1d(coefficients)

    # Generate x values for the trendline
    x_values = np.linspace(min(x), max(x), len(x))

    # Plot the trendline
    plt.plot(x_values, trendline(x_values), color=color)

    return coefficients


players_db = database.open_db("db/players.fs")
players_connection = database.get_connection(players_db)

# Process 4k players
leaderboard_db = database.open_db("db/leaderboard_4k.fs")
leaderboard_connection = database.get_connection(leaderboard_db)

scores_db = database.open_db("db/scores_4k.fs")
scores_connection = database.get_connection(scores_db)

ranks, top_n_plays_qr = get_scores(leaderboard_connection, scores_connection, players_connection, 30)

scores_connection.close()
scores_db.close()

leaderboard_connection.close()
leaderboard_db.close()

ranks, top_n_plays_qr = remove_outliers(ranks, top_n_plays_qr)
x, y = create_datasets(ranks, top_n_plays_qr, 10, 15)

# Plot data and write csv
plt.plot(x, y)
degree = 6
coefficients = generate_trendline(plt, x, y, degree, 'red')
plt.xlabel("Rank*")
plt.ylabel("Avg QR of Top 15")
plt.title("Rank vs. Average QR of Top 15 Plays (4k)")
plt.savefig("AvgQrTop15_vs_Rank_4k.png")
plt.clf()

data_as_columns = np.transpose(np.array([x, y]))
with open("AvgQrTop15_vs_Rank_4k.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_as_columns)

x = [(len(coefficients) - i - 1) for i in range(len(coefficients))]
data_as_columns = np.transpose(np.array([x, coefficients])).tolist()
for row in data_as_columns:
    row[0] = int(row[0])
with open("Trendline_coefficients_4k.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_as_columns)

# Process 7k players
leaderboard_db = database.open_db("db/testdb.fs")
leaderboard_connection = database.get_connection(leaderboard_db)

scores_db = database.open_db("db/scores_7k.fs")
scores_connection = database.get_connection(scores_db)

ranks, top_n_plays_qr = get_scores(leaderboard_connection, scores_connection, players_connection, 30)

scores_connection.close()
scores_db.close()

leaderboard_connection.close()
leaderboard_db.close()

players_connection.close()
players_db.close()

ranks, top_n_plays_qr = remove_outliers(ranks, top_n_plays_qr)
ranks, top_n_plays_qr = remove_outliers(ranks, top_n_plays_qr)
x, y = create_datasets(ranks, top_n_plays_qr, 10, 15)

# Plot data and write to csv
plt.plot(x, y)
degree = 6
coefficients = generate_trendline(plt, x, y, degree, 'red')
plt.xlabel("Rank*")
plt.ylabel("Avg QR of Top 15")
plt.title("Rank vs. Average QR of Top 15 Plays (7k)")
plt.savefig("AvgQrTop15_vs_Rank_7k.png")

data_as_columns = np.transpose(np.array([x, y]))
with open("AvgQrTop15_vs_Rank_7k.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_as_columns)

x = [(len(coefficients) - i - 1) for i in range(len(coefficients))]
data_as_columns = np.transpose(np.array([x, coefficients])).tolist()
for row in data_as_columns:
    row[0] = int(row[0])
with open("Trendline_coefficients_7k.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_as_columns)
