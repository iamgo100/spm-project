import tornado.ioloop
import tornado.web as web
import tornado.websocket
import asyncio
import json

import books as books_db

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
    
    def on_message(self, data):
        message = json.loads(data)
        if message["request"] == "open":
            con, cur = books_db.connecting()
            if message["page"] == "book":
                table = books_db.Books()
            if message["page"] == "series":
                table = books_db.Series()
            entry = books_db.select_entry(con, cur, table.name, message["id"])
            response = {}
            if entry[0]:
                for i in range(len(table.columns)):
                    if table.columns[i] == "author":
                        elem = books_db.select_entry(con, cur, books_db.Authors().name, entry[0][i+1])
                        value = []
                        for i in range(len(elem[0])-1):
                            if elem[0][i+1]:
                                value.append(elem[0][i+1])
                        elem = ' '.join(value)
                        response.update({"author": elem})
                    elif table.columns[i] == "interpreter":
                        elem = books_db.select_entry(con, cur, books_db.Interpreters().name, entry[0][i+1])
                        value = []
                        for i in range(len(elem[0])-1):
                            if elem[0][i+1]:
                                value.append(elem[0][i+1])
                        elem = ' '.join(value)
                        response.update({"interpreter": elem})
                    else:
                        elem = entry[0][i+1]
                        response.update({table.columns[i]: elem})
                response.update({"response": message["page"]})
            self.write_message(json.dumps(response))
    
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