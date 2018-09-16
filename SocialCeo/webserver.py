import tornado.ioloop
import tornado.web
import io
import sys
import numpy
from textblob import TextBlob

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        text = open("www/index.html").read()
        self.write(text)

class FileHandler(tornado.web.RequestHandler):
    def get(self, file):
        self.render("www/" + file)

class PredictionHandler(tornado.web.RequestHandler):
    def initialize(self, model):
        self.model = model

    def get(self):
        try:
            text = self.get_argument("text")
            retweets = float(self.get_argument("retweets"))
            favorites = float(self.get_argument("favorites"))

            blob = TextBlob(text)
            subjectivity = blob.sentiment.subjectivity
            polarity = blob.sentiment.polarity

            prediction = self.model.predict([[favorites, retweets, subjectivity, polarity]])

            self.write(str(prediction[0] * 100))
        except:
            print(5 / 0)
            self.send_error()

def run(model):
    app = tornado.web.Application([
        (r"/", RootHandler),
        (r"/predict/elon_musk", PredictionHandler, dict(model=model)),
        (r"/(.*)", FileHandler),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
