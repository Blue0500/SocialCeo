import tornado.ioloop
import tornado.web
import io

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        text = open("www/index.html").read()
        self.write(text)

class FileHandler(tornado.web.RequestHandler):
    def get(self, file):
        print(self.request.uri)
        text = open("www/" + file).read()

        self.write(text)

def run():
    app = tornado.web.Application([
        (r"/", RootHandler),
        (r"/(.*)", FileHandler),
    ])

    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
