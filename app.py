from flask import Flask, render_template, request, flash
import psycopg2
from pattern import check_pattern
#--------------------------------------------------------
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from connection import get_database_credentials_from_YAML
#--------------------------------------------------------

# Start Flask app
app = Flask(__name__)
app.secret_key = 'don tell anybody'


#--------------------------------------------------------
# connection = get_database_credentials_from_YAML()
# database_uri = f"{connection['database']}+{connection['database_dialect']}://{connection['user']}:{connection['password']}@{connection['host']}/{connection['database_name']}"


# print(database_uri)
#
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Mysqlbz8891751@localhost/sessions'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
# db = SQLAlchemy(app)
#
# print(connection)
# # Map to table
# # queryy = db.Table('sessions_to_comment', db.metadata, autoload=True, autoload_with=db.engine)
#
# schema = 'moma_reporting'
# # Map datatable to class
# Base = automap_base()
# engine = create_engine('postgresql+psycopg2://sxd:sxd@plsrvup-sxd01.ttg.global/statistics',connect_args={'options':'-csearch_path={}'.format(schema)})
# Base.prepare(engine, reflect=True)
# # table_name = f"Base.classes.{connection['table_name']}"
# Sessions = Base.classes.comments
# print(Sessions)
#--------------------------------------------------------


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


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/addComent', methods=['POST', 'GET'])
def addComment():
    if request.method == 'POST':
        if 'comment' in request.form:
            if request.form['text']:
                try:
                    connection_string = "dbname='statistics' user='sxd' host='plsrvup-sxd01.ttg.global' password='sxd'"
                    conn = psycopg2.connect(connection_string)
                    print("Database connected")
                except Exception as e:
                    print(e)
                list_of_sessions = request.form['text']
                comment_to_selects = request.form['option']
                sessions_without_quote = list_of_sessions.replace("'", '').replace('\r\n', '\n').replace('"', '')
                result = prepareSessions(sessions_without_quote)
                correct_sessions = [session.strip() for session in result if session]
                # update session's comment
                cur = conn.cursor()
                sessions_exists_in_database = []
                sessions = check_pattern(correct_sessions)
                wrongs = list(set(correct_sessions).difference(set(sessions)))
                for session in sessions:
                    cur.execute(f"""SELECT * FROM moma_reporting.comments WHERE "sessionname" LIKE '{session}'""")
                    result= cur.fetchone()
                    if result is not None:
                        cur.execute(
                            f"""UPDATE moma_reporting.comments SET comment = '{comment_to_selects}' WHERE sessionname like '{session}'""")
                        conn.commit()
                        sessions_exists_in_database.append(session)
                    elif result is None:
                        cur.execute(
                            f"""INSERT INTO moma_reporting.comments VALUES ('{session}','{comment_to_selects}')""")
                        conn.commit()
                        sessions_exists_in_database.append(session)
                cur.close()
                good_sessions_len = len(sessions_exists_in_database)
                if len(wrongs) > 0:
                    flash(
                        f"You have just commented {good_sessions_len} sessions and have {len(wrongs)} issue(s)",
                        'warning')
                else:
                    flash(f"You have just commented {good_sessions_len} sessions", 'success')
            else:
                flash("You didn't provide sessions amigo", 'warning')
                return render_template('index.html')
        return render_template('index.html', sessions_exists_in_database=sessions_exists_in_database,
                               wrongs=wrongs, option=comment_to_selects)


if __name__ == '__name__':
    app.run(DEBUG=True)


