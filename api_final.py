import flask
from flask import request, jsonify
import sqlite3
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#home
@app.route('/', methods=['GET'])
def home():
    return """<body style="margin:0; font-weight: 100;letter-spacing: 0.036em;background: #eae4da;color: #000; text-align:center;">
                <h2 style="color: #000; background:#b8cc8c; margin:0; padding-top:30px; padding-bottom:10px; text-transform: uppercase; font-weight: 200;letter-spacing: 5.99px;">Books API</h2>
                <p>This api must be used for consultation and data registration for the book application developed</p>
                <h3 style="font-weight: 200; background:#e4c7ce; padding: 10px 0 10px 0">USAGE - ROUTES</h3>
                <div style="display: flex; align-items:center; justify-content: center;">
                <ul style="text-align:left">
                <li>/books</li>
                    <ul><li>REQUIRED: id or published or author [GET]</li></ul>
                <li>/books/:id</li>
                    <ul><li>METHODS: DELETE, PATCH</li></ul>
                <li>/books/all</li>
                <li>/addBook</li>
                </ul>
                </div>
            
            <body>"""


#INSERT book
@app.route('/addBook', methods=['POST'])
def register():
    request.get_json(force=True)
    query_parameters = request.json
    title = (query_parameters.get('title'))
    author = (query_parameters.get('author'))
    status = (query_parameters.get('status'))
    classification = (query_parameters.get('classification'))

    
    try:
        sqliteConnection = sqlite3.connect('books.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_insert_query = f"""INSERT INTO books
                              (title, author, status, classification) 
                               VALUES 
                              ('{title}','{author}',{status},{classification})"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return '''<h2>Cadastro de livros</h2>'''


#List all
@app.route('/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


#error handler
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#search method
@app.route('/books', methods=['GET'])
def api_filter():
    query_parameters = request.args
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


#DELETE method
@app.route('/books/<id>', methods=['DELETE'])
def delete(id):
    try:
        sqliteConnection = sqlite3.connect('books.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_delete_query = f"""DELETE FROM books WHERE id = {id}"""

        count = cursor.execute(sqlite_delete_query)
        sqliteConnection.commit()
        print("Record deleted.", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete data ", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("The SQLite connection is closed")

    return '{mensage: "File deleted."}'

#ALTER method
@app.route('/books/<id>', methods=['PATCH'])
def alter(id):
    request.get_json(force=True)
    query_parameters = request.json
    title = (query_parameters.get('title'))
    author = (query_parameters.get('author'))
    status = (query_parameters.get('status'))
    classification = (query_parameters.get('classification'))

    try:
        sqliteConnection = sqlite3.connect('books.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_alter_query = f"""UPDATE books
                                    SET title = '{title}',
                                        author = '{author}',
                                        status = {status},
                                        classification = {classification}
                                 WHERE id = {id}"""

        count = cursor.execute(sqlite_alter_query)
        sqliteConnection.commit()
        print("Record altered.", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to alter data ", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("The SQLite connection is closed")

    return '{mensage: "File altered."}'


app.run()
