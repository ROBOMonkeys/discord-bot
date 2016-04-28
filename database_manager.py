import sqlite3 as sql

c = sql.connect('quotes.db')


def add_quote(author, msg):
    c.execute('''INSERT INTO quotes VALUES (NULL, %s, %s)''' % (author, msg))
    c.commit()


def get_quote(author, num=1):
    quotes = c.execute('''SELECT message FROM quotes WHERE author == '%s' ''' % author).fetchall()
    return quotes[:num]

try:
    c.execute('''SELECT * FROM quotes''').fetchone()
except sql.OperationalError:
    c.execute('''CREATE TABLE quotes(id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, message TEXT)''')
    c.commit()
