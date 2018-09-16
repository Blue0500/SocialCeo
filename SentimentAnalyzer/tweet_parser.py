from textblob import TextBlob
import io
import csv
import dateutil.parser as date_parse
import stockchange

tweet_info = { }
with open("Tweets.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in list(reader)[1:]:
        text = row.pop("Text")
        blob = TextBlob(text)

        # Calculate subjectivity and polarity
        row["Subjectivity"] = blob.subjectivity
        row["Polarity"] = blob.polarity #(blob.polarity + 1) / 2
        
        row["Favorites"] = float(row["Favorites"])
        row["Retweets"] = float(row["Retweets"])

        date = row.pop("Date") #date_parse.parse(row.pop("Date")).strftime("%Y-%d-%m")
        if date in tweet_info:
            tweet_info[date].append(row)
        else:
            tweet_info[date] = [row]

aggregate_info = []
for (date, info) in tweet_info.items():
    total_retweets = 0
    total_favorites = 0

    for tweet in info:
        total_retweets += tweet["Retweets"]
        total_favorites += tweet["Favorites"]

    total_value = total_retweets + total_favorites
    total_polarity = 0
    total_subjectivity = 0

    for tweet in info:
        value = tweet["Retweets"] + tweet["Favorites"]

        total_subjectivity += tweet["Subjectivity"] * value / total_value
        total_polarity += tweet["Polarity"] * value / total_value

    aggregate_info.append([date, total_retweets, total_favorites, total_subjectivity, total_polarity])

csv_rows = []
stock_changes = stockchange.get_dates("HistoricalQuotes.csv")

for info in aggregate_info:
    if info[0] in stock_changes:            
        info[0] = stock_changes[info[0]]
        csv_rows.append(info)

with open('Tweets_out.csv', mode='w', encoding="utf-8") as out_file:
    writer = csv.writer(out_file, lineterminator='\n')
    writer.writerow(["PercentChange", "Retweets", "Favorites", "Subjectivity", "Polarity"])

    for row in csv_rows:
        writer.writerow(row)