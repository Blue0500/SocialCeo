import io
import csv

X_data = []
Y_data = []

with open("Tweets_out.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in list(reader)[1:]:
        X_data.append(row.pop(0))
        Y_data.append(row)

