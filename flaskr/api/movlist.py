from flask import jsonify, request, url_for, g
from . import api
from ..tools import db_tool, other


@api.route('/movlists/<int:id>')
def get_movlist(id):
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info WHERE id IN (SELECT movie_id FROM movlist_movie WHERE movlist_id = %s)"
        count = db_tool.print_and_try(cursor, sql, id)
        movies = cursor.fetchall()
    for movie in movies:
        movie['release_date'] = other.date_string(movie['release_date'])
    print(movies)
    return jsonify({
        "count" : count,
        "movies" : movies
    })

@api.route('/movlists')
def get_movlists():
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movlist ORDER BY create_time DESC LIMIT 0, 20"
        movlist_count = db_tool.print_and_try(cursor, sql)
        movlists = cursor.fetchall()
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info WHERE id IN (SELECT movie_id FROM movlist_movie WHERE movlist_id = %s)"
        for movlist in movlists:
            movie_count = db_tool.print_and_try(cursor, sql, movlist["id"])
            movies = cursor.fetchall()
            for movie in movies:
                movie['release_date'] = other.date_string(movie['release_date'])
            movlist["count"] = movie_count
            movlist["movies"] = movies
    print(movlists)
    return jsonify({
        "count" : movlist_count,
        "movlists" : movlists
    })

@api.route('/movlists', methods=['POST'])
def post_movlist():
    data = request.get_json()
    user_id = other.verify_token(other.get_request_token())
    print(user_id)
    title = data.get('title')
    with db_tool.get_cursor() as cursor:
        sql = "INSERT INTO movlist (user_id, title) VALUES (%s, %s)"
        db_tool.print_and_try(cursor, sql, (user_id, title))
    return jsonify({"message" : 'ok'})


@api.route('/movlists/<int:movlist_id>/movies', methods=['POST'])
def post_movlist_movie(movlist_id):
    data = request.get_json()
    movie_id = data.get('movie_id')
    user_id = other.verify_token(other.get_request_token())
    with db_tool.get_cursor() as cursor:
        sql = "INSERT INTO movlist_movie (movlist_id, movie_id) VALUES (%s, %s)"
        db_tool.print_and_try(cursor, sql, (movlist_id, movie_id))
    return jsonify({"message" : 'ok'})

@api.route('/movlists/<int:movlist_id>/movies', methods=['DELETE'])
def delete_movlist_movie(movlist_id):
    data = request.get_json()
    movie_id = data.get('movie_id')
    user_id = other.verify_token(other.get_request_token())
    with db_tool.get_cursor() as cursor:
        sql = "DELETE FROM movlist_movie WHERE movlist_id = %s AND movie_id = %s"
        db_tool.print_and_try(cursor, sql, (movlist_id, movie_id))
    return jsonify({"message" : 'ok'})
