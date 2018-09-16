import csv

changes = []
days = []
stocks = []

with open('tsla.us.txt', 'r') as csvfile:
    reader = csv.reader(csvfile)
    #row_count = sum(1 for row in csvfile)
    for row in reader:
        stocks.append(row)
        if len(stocks) > 2:
            percent_difference = (float(stocks[-1][1]) - float(stocks[-2][1]))/float(stocks[-2][1]) * 100
            changes.append(percent_difference)
            days.append(stocks[-2][0])


cumulative = (list(zip(days, changes)))


with open('changes.csv', 'w') as csvfile:
    changewriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    for i in range(len(cumulative)):
        changewriter.writerow(cumulative[i])