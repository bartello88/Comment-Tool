from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from connection import getDatabaseCredentialsFromYAML

# Start Flask app
app = Flask(__name__)

connection = getDatabaseCredentialsFromYAML()
database_uri = f"{connection['database']}+{connection['database_dialect']}://{connection['user']}:{connection['password']}@{connection['host']}/{connection['databasename']}"
app.secret_key = 'don tell anybody'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Mysqlbz8891751@localhost/sessions'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)

# Map to table
# queryy = db.Table('sessions_to_comment', db.metadata, autoload=True, autoload_with=db.engine)


# Map datatable to class
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Sessions = Base.classes.sessions_to_comment


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/addComent', methods=['POST', 'GET'])
def addComment():
    if request.method == 'POST':
        if 'comment' in request.form:
            if request.form['text']:
                list_of_sessions = request.form['text']
                comment_to_selects = request.form['option']
                sessions_without_quote = list_of_sessions.replace("'", '').replace('\r\n', '\n').replace('"', '')
                result = prepareSessions(sessions_without_quote)
                correct_sessions = [session.strip() for session in result if session]

                # update session's comment
                wrong_sessions = []
                sessions_exists_in_database = []
                for session in correct_sessions:
                    try:
                        if db.session.query(Sessions).filter_by(session_name=session).first() is not None:
                            conn = db.session.query(Sessions).filter_by(session_name=session).first()
                            conn.session_comment = comment_to_selects
                            db.session.commit()
                            print(f"Session {session} has been commented sucessfully")
                            sessions_exists_in_database.append(session)
                        else:
                            print(f"Session {session} doesn't exists")
                            wrong_sessions.append(session)
                    except AttributeError as e:
                        print(e)
                good_sessions_len = len(sessions_exists_in_database)
                if len(wrong_sessions) > 0:
                    flash(
                        f"You have just commented {good_sessions_len} sessions and have {len(wrong_sessions)} issue(s)",
                        'warning')
                else:
                    flash(f"You have just commented {good_sessions_len} sessions", 'success')
            else:
                flash("You didn't provide sessions amigo", 'error')
                return render_template('index.html')

        return render_template('index.html', sessions_exists_in_database=sessions_exists_in_database,
                               wrong_sessions=wrong_sessions, option=comment_to_selects)

# Getting current list of sessions
def prepareSessions(sessions_without_quote):
    if ', ' in sessions_without_quote:
        result = sessions_without_quote.split(', ')
    elif ',' in sessions_without_quote:
        result = sessions_without_quote.split(',')
    elif '\t' in sessions_without_quote:
        result = sessions_without_quote.split('\t')
    elif '\n' in sessions_without_quote:
        result = sessions_without_quote.split('\n')
    else:
        result = sessions_without_quote.split(' ')

    return result

def something():
    pass