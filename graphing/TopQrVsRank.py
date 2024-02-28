import matplotlib.pyplot as plt
import csv
import database
import numpy as np


def create_datasets(leaderboard_connection, scores_connection, player_connection, stride, num_of_scores):
    rank_bins = []
    average_top15_qr = []

    root = leaderboard_connection.root()
    batch_count = len(root.keys()) // stride
    for batch in range(batch_count):
        batch_averages = []
        for i in range(stride):
            player_id = database.get_player_id_by_rank(leaderboard_connection, batch * stride + i + 1)
            player = database.get_player(player_connection, player_id)
            print("Current player:", player["info"]["username"])
            scores = database.get_scores_by_id(scores_connection, player_id)
            
            sum = 0
            scores_counted = 0
            for k in range(num_of_scores):
                if k < len(scores):
                    sum += scores[k]["performance_rating"]
                    scores_counted += 1
            
            if scores_counted > 0:
                batch_averages.append(sum / scores_counted)

        # print(batch_averages)
        sum = 0
        for average in batch_averages:
            sum += average

        average_top15_qr.append(sum / len(batch_averages))
        rank_bins.append((batch + 1) * stride)

    return rank_bins, average_top15_qr


players_db = database.open_db("db/players.fs")
players_connection = database.get_connection(players_db)

# Process 4k players
leaderboard_db = database.open_db("db/leaderboard_4k.fs")
leaderboard_connection = database.get_connection(leaderboard_db)

scores_db = database.open_db("db/scores_4k.fs")
scores_connection = database.get_connection(scores_db)

x, y = create_datasets(leaderboard_connection, scores_connection, players_connection, 10, 15)
plt.plot(x, y)
plt.xlabel("Rank*")
plt.ylabel("Avg QR of Top 15")
plt.title("Rank vs. Average QR of Top 15 Plays (4k)")
plt.savefig("AvgQrTop15_vs_Rank_4k.png")
plt.clf()

data_as_columns = np.transpose(np.array([x, y]))
with open("AvgQrTop15_vs_Rank_4k.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_as_columns)

scores_connection.close()
scores_db.close()

leaderboard_connection.close()
leaderboard_db.close()

# Process 7k players
leaderboard_db = database.open_db("db/testdb.fs")
leaderboard_connection = database.get_connection(leaderboard_db)

scores_db = database.open_db("db/scores_7k.fs")
scores_connection = database.get_connection(scores_db)

x, y = create_datasets(leaderboard_connection, scores_connection, players_connection, 10, 15)
plt.plot(x, y)
plt.xlabel("Rank*")
plt.ylabel("Avg QR of Top 15")
plt.title("Rank vs. Average QR of Top 15 Plays (7k)")
plt.savefig("AvgQrTop15_vs_Rank_7k.png")

data_as_columns = np.transpose(np.array([x, y]))
with open("AvgQrTop15_vs_Rank_7k.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_as_columns)

players_connection.close()
players_db.close()

