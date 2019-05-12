from . import api
from ..tools import db_tool, other
from flask import request, abort, jsonify

@api.route('/movies/<int:id>')
def get_movie(id):
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info WHERE id = %s"
        if db_tool.print_and_try(cursor, sql, id) == 0:
            abort(404)
        movie = cursor.fetchone()
    movie['release_date'] = other.date_string(movie['release_date'])
    print(movie)
    return jsonify({'movie' : movie})


@api.route('/movies')
def get_movies():
    args = request.args
    order_by = args.get('order_by') or 'id'
    order = args.get('order') or 'DESC'
    offset = int(args.get('offset')) if args.get('offset') else 0
    count = int(args.get('count')) if args.get('count') else 20
    sql = "SELECT * FROM movie_info  ORDER BY %s %s " % (order_by, order) + "LIMIT %s, %s"
    with db_tool.get_cursor() as cursor:
        real_count = db_tool.print_and_try(cursor, sql, (offset, count))
        movies = cursor.fetchall()
    for movie in movies:
        movie['release_date'] = other.date_string(movie['release_date'])
    return jsonify({
        'count' : real_count,
        'movies' : movies
    })

@api.route('/movies/search')
def movie_search():
    args = request.args
    q = "%%%s%%" % args.get('q')
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info WHERE title LIKE %s OR original_title LIKE %s"
        count = db_tool.print_and_try(cursor, sql, (q, q))
        movies = cursor.fetchall()
    return jsonify({
        "count" : count,
        "movies" : movies
    })

