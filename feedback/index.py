from flask import Flask, render_template, request, g
import sqlite3


app = Flask(__name__)
DATABASE = 'feedback.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/feedback/', methods=['POST', 'GET'])
def feedback():
    context = {}
    if request.method == 'POST':
        query = f'update {request.data}'  # TODO write the update query for adding feedback
        query_db(query)

    # Do on get and post
    query = f'select * from clips join feedback f'  # TODO write the select query for getting the next item
    clip = query_db(query, one=True)
    context['clip_path'] = clip.path
    context['clip_text'] = clip.text
    return render_template('feedback.html', context=context)

