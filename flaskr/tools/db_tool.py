import pymysql
from flask import current_app, g, abort

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            current_app.config['DB_HOST'],
            current_app.config['DB_USER'],
            current_app.config['DB_PASSWORD'],
            current_app.config['DB_NAME'],
            autocommit = True
        )
    return g.db



def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

def get_cursor():
    return get_db().cursor(cursor=pymysql.cursors.DictCursor)


def print_and_try(cursor, sql, args=None):
    try:
        sql_mogrify = cursor.mogrify(sql, args)
        print(sql_mogrify)
        effect_row = cursor.execute(sql_mogrify)
    except Exception as e:
        print('e: %s' % e)
        g.db.rollback()
        abort(500)
    return effect_row
        