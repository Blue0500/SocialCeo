from textblob import TextBlob
import io
import csv
import dateutil.parser as date_parse
import os.path as path

def parse_tweet_data(tweet_file):
    tweet_info = { }

    with open(tweet_file, encoding="utf-8") as file:
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

    return tweet_info

def parse_stock_data(stock_file):
    changes = []
    days = []
    stocks = []

    with open(stock_file, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            stocks.append(row)
            if len(stocks) > 2:
                percent_difference = (float(stocks[-1][1]) - float(stocks[-2][1]))/float(stocks[-2][1])
                changes.append(percent_difference)
                days.append(stocks[-2][0])
    
    return dict(zip(days, changes))

def fold_tweet_data(tweet_data):
    aggregate_info = []

    for (date, info) in tweet_data.items():
        total_retweets = 0
        total_favorites = 0

        # Total the retweets and favorites
        for tweet in info:
            total_retweets += tweet["Retweets"]
            total_favorites += tweet["Favorites"]

        total_value = total_retweets + total_favorites
        total_polarity = 0
        total_subjectivity = 0

        # Calculate a weighted average for subjectivity and polarity
        for tweet in info:
            value = tweet["Retweets"] + tweet["Favorites"]

            total_subjectivity += tweet["Subjectivity"] * value / total_value
            total_polarity += tweet["Polarity"] * value / total_value

        # Append the aggregated data as a row
        aggregate_info.append([date, total_retweets, total_favorites, total_subjectivity, total_polarity])

    return aggregate_info

def aggregate_tweets_stocks(tweet_data, stock_data):
    rows = []

    for data in tweet_data:
        if data[0] in stock_data:            
            data[0] = stock_data[data[0]]
            rows.append(data)

    return rows

def generate_data(ceo):
    tweet_file = "data/tweets/" + ceo + ".csv"
    stock_file = "data/stocks/" + ceo + ".csv"
    combined_file = "data/combined/" + ceo + ".csv"

    """
    if path.isfile(combined_file):
        with open(combined_file, encoding="utf-8") as file:
            reader = csv.DictReader(file)

    else:
        tweets = fold_tweet_data(parse_tweet_data(tweet_file))
        stocks = parse_stock_data(stock_file)

        with open(combined_file, encoding="utf-8") as file:
            writer = csv.writer(file)
    """

    tweets = fold_tweet_data(parse_tweet_data(tweet_file))
    stocks = parse_stock_data(stock_file)
    return aggregate_tweets_stocks(tweets, stocks)