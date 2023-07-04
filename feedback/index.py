from flask import Flask, render_template, request, g, session, redirect, url_for
import sqlite3
import ast

from zu_ipa import syllablize
import secret


app = Flask(__name__)
DATABASE = secret.DATABASE
# Set this up for yourself do NOT push to git
app.secret_key = secret.SECRET_KEY


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread = False)
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()
    return


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/", methods=['POST', 'GET'])
def index():
    message = 'What is your grader id?'

    # Handle form submission
    if request.method == 'POST':
        graderid = request.form['name']
        # check if the speaker is in the db
        query = f'select speakerid from speakers where speakerid = {graderid};'
        if query_db(query):  # grader is in the db
            session["graderid"] = graderid  # maintains the graderid across the requests
            return redirect(url_for('feedback'))
        else:  # the grader is not in the db, ask again
            message = 'Sorry, we could not find that grader id. Please try again:'

    return render_template('index.html', message = message)


@app.route('/feedback/', methods=['POST', 'GET'])
def feedback():

    if 'graderid' not in session:  # make sure that a graderid is always active
        return redirect(url_for('index'))

    # Handle form submission
    if request.method == 'POST':
        errors = [int(x) for x in request.form.getlist('errors')]
        errors_tone = [x for x in request.form.getlist('errors_tone')]
        errors_insert = request.form.getlist('inserts')
        feedback = ['1' for _ in range(len(ast.literal_eval(request.form['clip_text'])))]
        for x in errors:
            feedback[x] = '0'

        # Insert the feedback into the table
        query = f"insert into feedback (clip, grader, scores, scores_tones) " \
                f"values ('{request.form['clip_path']}', {session['graderid']}, " \
                f"'{''.join(feedback)}', '{''.join(errors_tone)}');"
        insert_db(query)

    # Do following on get and post

    # This (should) gets all clips that have not been graded by the session grader
    query = f'select c.* from clips c where filename not in ' \
            f'(select clip from feedback where grader = {session["graderid"]}) ' \
            f'order by random() limit 1;'
    clip = query_db(query, one=True)
    # (filename, sentence, speakerid)

    if not clip:
        return redirect(url_for('finished'))

    clip_syl, clip_text = syllablize(clip[1])

    spans = []
    j = 0
    for s in clip_syl:
        x = 0
        y = 0
        if not s:
            j += 1
            y += 1
        else:
            while x < len(s):
                x += len(clip_text[j])
                j += 1
                y += 1
        spans.append(y)

    return render_template('feedback.html', org_text = clip[1], clip_path = clip[0], clip_text = clip_text,
                           syl_spans = spans)


@app.route('/finished/')
def finished():
    return render_template('finished.html', message = "We couldn't find any more clips to score, so you are finished! "
                                                      "Thank you so much for your help. "
                                                      "Please let Alex and/or Nils know. ")
