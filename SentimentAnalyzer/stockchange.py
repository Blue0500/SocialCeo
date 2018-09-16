import csv

def get_dates(file):
    changes = []
    days = []
    stocks = []

    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            stocks.append(row)
            if len(stocks) > 2:
                percent_difference = (float(stocks[-1][1]) - float(stocks[-2][1]))/float(stocks[-2][1]) * 100
                changes.append(percent_difference)
                days.append(stocks[-2][0])

    cumulative = (dict(zip(days, changes)))
    return cumulative