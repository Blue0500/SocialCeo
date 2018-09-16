import tweet_parser
import models
import webserver
import math

def elon_musk_data():
    return tweet_parser.generate_data("elon_musk")

print("Initalizing data for server")
data = elon_musk_data()
model = models.init(data)

print("Server running")
webserver.run(model)