import sqlite3

class Books:
    name = "books"
    headers = [
        "название",
        "автор (id)",
        "переводчик (id)",
        "издательство",
        "год",
        "аннотация",
        "обложка (ссылка)",
        "серия (ссылка)",
        "часть (число)",
        "экранизация"
    ]
    columns = [
        "name",
        "author",
        "interpreter",
        "p_office",
        "year",
        "annotation",
        "pict",
        "series",
        "part",
        "film_adapt"
    ]

class Series:
    name = "serie_s"
    headers = [
        "название",
        "автор (id)",
        "переводчик (id)",
        "издательство",
        "аннотация",
        "хроника"
    ]
    columns = [
        "name",
        "author",
        "interpreter",
        "p_office",
        "annotation",
        "sequence"
    ]

class Authors:
    name = "authors"
    headers = [
        "fname",
        "sname",
        "lname"
    ]
    columns = [
        "fname",
        "sname",
        "lname"
    ]

class Interpreters:
    name = "interpreters"
    headers = [
        "fname",
        "sname",
        "lname"
    ]
    columns = [
        "fname",
        "sname",
        "lname"
    ]

def create_tables(con):

    con.execute('PRAGMA foreign_keys = on')
    con.commit()

    con.execute(
        '''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NOT NULL,
            sname TEXT,
            lname TEXT NOT NULL
        )
        '''
    )
    con.commit()

    con.execute(
        '''
        CREATE TABLE IF NOT EXISTS interpreters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT,
            sname TEXT,
            lname TEXT NOT NULL
        )
        '''
    )
    con.commit()

    # con.execute(
    #     '''
    #     CREATE TABLE IF NOT EXISTS dif_inf_table (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         b_s_id INTEGER NOT NULL,
    #         block_i TEXT,
    #         FOREIGN KEY (b_s_id) REFERENCES books(id) ON UPDATE CASCADE ON DELETE CASCADE,
    #         FOREIGN KEY (b_s_id) REFERENCES series(id) ON UPDATE CASCADE ON DELETE CASCADE
    #     )
    #     '''
    # )

    con.execute(
        '''
        CREATE TABLE IF NOT EXISTS serie_s (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author INTEGER NOT NULL,
            interpreter INTEGER,
            p_office TEXT NOT NULL,
            annotation TEXT NOT NULL,
            sequence TEXT NOT NULL,
            FOREIGN KEY (author) REFERENCES authors(id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (interpreter) REFERENCES interpreters(id) ON UPDATE CASCADE ON DELETE CASCADE
        )
        '''
    )
    con.commit()

    con.execute(
        '''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author INTEGER NOT NULL,
            interpreter INTEGER,
            p_office TEXT NOT NULL,
            year INTEGER NOT NULL,
            annotation TEXT NOT NULL,
            pict TEXT,
            series TEXT,
            part INTEGER,
            film_adapt TEXT,
            FOREIGN KEY (author) REFERENCES authors(id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (interpreter) REFERENCES interpreters(id) ON UPDATE CASCADE ON DELETE CASCADE
        )
        '''
    )
    con.commit()

def add_entry(con, cur):
    while True:
        t = input("table: ")
        if t == "books":
            cl = Books(); break
        elif t == "series":
            cl = Series(); break
        elif t == "authors":
            cl = Authors(); break
        elif t == "inter":
            cl = Interpreters(); break
        else:
            print('ошибка')
    table = cl.name
    columns = []
    values = []
    for i in range(len(cl.headers)):
        val = input(f"{cl.headers[i]}: ")
        if val:
            columns.append(cl.columns[i])
            values.append(val)
    columns = (',').join(columns)
    values = ('","').join(values)
    query = f'INSERT INTO {table} ({columns}) VALUES ("{values}")'
    try:
        print(query)
        cur.execute(query)
    except sqlite3.Error as e:
        print(f'Ошибка добавления: {e}\n')
    else:
        print('Запись успешно добавлена\n')
        con.commit()

if __name__ == "__main__":

    con = sqlite3.connect('books.db')
    cur = con.cursor()

    try:
        create_tables(con)
    except sqlite3.Error as e:
        print(f'Ошибка: {e}')
    
    # add_entry(con, cur)
    # table = input("table: ")
    # res = []
    # query = f'SELECT * FROM authors'
    # res.append(cur.execute(query).fetchall())
    # query = f'SELECT * FROM interpreters'
    # res.append(cur.execute(query).fetchall())
    # query = f'SELECT * FROM books'
    # res.append(cur.execute(query).fetchall())
    # print(res)
