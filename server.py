import tornado.ioloop
import tornado.web as web
import tornado.websocket
import asyncio
import json

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')

class BookHandler(web.RequestHandler):
    def get(self):
        self.render('book.html')

class SeriesHandler(web.RequestHandler):
    def get(self):
        self.render('series.html')

class MainHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('open')
    
    def on_message(self):
        pass
    
    def on_close(self):
        print('close')

def make_app():
    return web.Application([
        (r"/", IndexHandler),
        (r"/book", BookHandler),
        (r"/series", SeriesHandler),
        (r"/websocket", MainHandler),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8080, 'localhost')
    tornado.ioloop.IOLoop.current().start()