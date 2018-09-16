import io
import csv
import models

X_data = []
Y_data = []

with open("Tweets_out.csv", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in list(reader)[1:]:
        Y_data.append(float(row.pop(0)))
        X_data.append(list(map(lambda x: float(x), row)))

models.model(X_data, Y_data)