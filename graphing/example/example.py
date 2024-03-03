import matplotlib.pyplot as plt
import csv
 
# Creating data
x = ['2010', '2002', '2004', '2006', '2008']
y = [10, 25, 50, 15, 8]

with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows([x, y])

# Plotting barchart
plt.bar(x, y)
 
# Saving the figure.
plt.savefig("output-1.jpg")