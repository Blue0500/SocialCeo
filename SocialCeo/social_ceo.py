import tweet_parser
import models
import webserver
import math

def elon_musk_data():
    return tweet_parser.generate_data("elon_musk")

webserver.run();

#data = elon_musk_data()
#models.run(data)

