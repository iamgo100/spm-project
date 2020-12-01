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
        "cover",
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
            cover TEXT,
            series TEXT,
            part INTEGER,
            film_adapt TEXT,
            FOREIGN KEY (author) REFERENCES authors(id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (interpreter) REFERENCES interpreters(id) ON UPDATE CASCADE ON DELETE CASCADE
        )
        '''
    )
    con.commit()

def make_entry(tcl):
    columns = []
    values = []
    for i in range(len(tcl.headers)):
        val = input(f"{tcl.headers[i]}: ")
        if val:
            columns.append(tcl.columns[i])
            values.append(val)
    columns = (',').join(columns)
    values = ('","').join(values)
    return columns, values

def add_entry(con, cur, tcl):
    columns, values = make_entry(tcl)
    query = f'INSERT INTO {tcl.name} ({columns}) VALUES ("{values}")'
    try:
        print(query)
        cur.execute(query)
    except sqlite3.Error as e:
        print(f'Ошибка добавления: {e}\n')
    else:
        print('Запись успешно добавлена\n')
        con.commit()

def change_entry(con, cur, tcl, key):
    columns, values = make_entry(tcl)
    query = f'UPDATE {tcl.name} SET ({columns}) = ("{values}") WHERE id = "{key}"'
    try:
        print(query)
        cur.execute(query)
    except sqlite3.Error as e:
        print(f'Ошибка изменения: {e}\n')
    else:
        print('Запись успешно изменена\n')
        con.commit()

def delete_entry(con, cur, table, key):
    query = f'DELETE FROM {table} WHERE id = "{key}"'
    try:
        print(query)
        cur.execute(query)
    except sqlite3.Error as e:
        print(f'Ошибка удаления: {e}\n')
    else:
        print('Запись успешно удалена\n')
        con.commit()

def select_entry(con, cur, table, key):
    query = f'SELECT * FROM {table} WHERE id = "{key}"'
    try:
        print(query)
        res = cur.execute(query).fetchall()
    except sqlite3.Error as e:
        print(f'Ошибка поиска: {e}\n')
    else:
        con.commit()
        return res

def connecting():
    try:
        con = sqlite3.connect('books.db')
        cur = con.cursor()
        create_tables(con)
        return con, cur
    except sqlite3.Error as e:
        print(f'Ошибка: {e}')
        return

if __name__ == "__main__":
    pass