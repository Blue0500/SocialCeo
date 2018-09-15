
import pandas as pd
import csv

table = pd.read_csv('tsla.us.txt')
stocks = table['Open']
days = table['Date']
change = []

for i in range(len(stocks)-1):
    percent_difference = (stocks[i+1] - stocks[i])/(stocks[i]) * 100
    change.append(percent_difference)




with open('changes.csv', 'wb', newline = '') as csvfile:
    changewriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(stocks)-1):
        changewriter.writerow(zip(days[i], stocks[i]))




