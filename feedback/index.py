from flask import Flask, render_template, request, g, session, redirect, url_for
import sqlite3

from zu_ipa import syllablize


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


@app.route("/", methods=['POST', 'GET'])
def index():
    context = {'message': 'What is your grader id?'}
    if request.method == 'POST':
        graderid = request.form['name']
        # check if the speaker is in the db
        query = f'select speakerid from speakers where speakerid = {graderid};'
        if query_db(query):  # grader is in the db
            session["graderid"] = graderid  # maintains the graderid across the requests
            return redirect(url_for('feedback'))
        else:  # the grader is not in the db, ask again
            context['message'] = 'Sorry, we could not find that grader id. Please try again:'
    return render_template('index.html', context = context)


@app.route('/feedback/', methods=['POST', 'GET'])
def feedback():
    context = {}
    if request.method == 'POST':
        errors = [int(x) for x in request.form['errors']]
        feedback = [1 for _ in range(len(request.form['clip_text']))]
        for x in errors:
            feedback[x] = 0
        # Insert the feedback into the table
        query = f'insert into feedback (clip, graderid, feedback) ' \
                f'values ({request.form["clip_path"]}, {session["graderid"]}, {str(feedback)});'
        query_db(query)

    # Do following on get and post

    # This (should) gets all clips that have not been graded by the session grader
    query = f'select c.* from clips c where filename not in ' \
            f'(select filename from feedback where grader = {session["graderid"]}) ' \
            f'order by random() limit 1;'

    clip = query_db(query, one=True)
    context['clip_path'] = clip.filename
    context['clip_text'] = syllablize(clip.text)
    return render_template('feedback.html', context = context)

