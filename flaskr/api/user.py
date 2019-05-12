from flask import jsonify, request, url_for
from . import api
from ..tools import db_tool,other


@api.route('/users', methods = ['POST'])
def post_user():
    data = request.get_json()
    email = data.get('email')
    nm = data.get('nm')
    pwd = data.get('pwd')
    with db_tool.get_cursor() as cursor:
        sql = "SELECT 1 FROM user_info WHERE email = %s "
        if db_tool.print_and_try(cursor, sql, email) > 0:
            return jsonify({'message': 'This email has already been registered'})
    with db_tool.get_cursor() as cursor:
        sql = "INSERT INTO user_info (email, nm, pwd) VALUES (%s, %s, %s)"
        if db_tool.print_and_try(cursor, sql, (email, nm, pwd)) == 1:
            return jsonify({'message': 'ok'})
        return jsonify({'message': 'error'})


@api.route('/users/<int:user_id>/movlists')
def get_user_movlist(user_id):
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movlist WHERE user_id = %s ORDER BY create_time DESC"
        movlist_count = db_tool.print_and_try(cursor, sql, user_id)
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

@api.route('/users/<int:user_id>/collection_movies')
def get_user_collection_movies(user_id):
    token = other.get_request_token()
    user_id = other.verify_token(token)
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info WHERE id IN (SELECT movie_id FROM collection_movie WHERE user_id = %s)"
        count = db_tool.print_and_try(cursor, sql, user_id)
        movies = cursor.fetchall()
    for movie in movies:
        movie['release_date'] = other.date_string(movie['release_date'])
    return jsonify({
        "count" : count,
        "movies" : movies
    })

@api.route('/users/<int:user_id>/collection_movies/<int:movie_id>')
def get_user_collection_movie(user_id, movie_id):
    token = other.get_request_token()
    user_id = other.verify_token(token)
    print(user_id)
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM collection_movie WHERE user_id = %s AND movie_id = %s"
        count = db_tool.print_and_try(cursor, sql, (user_id, movie_id))
        detial = cursor.fetchone()
        print(detial)
    return jsonify({
        "count" : count,
        "detial" : detial
    })

@api.route('/users/<int:user_id>/collection_movies', methods=["POST"])
def post_user_collection_movie(user_id):
    token = other.get_request_token()
    user_id = other.verify_token(token)
    print(user_id)
    data = request.get_json()
    movie_id = data.get('movie_id')
    print(movie_id)
    with db_tool.get_cursor() as cursor:
        sql = "INSERT INTO collection_movie (user_id, movie_id) VALUES (%s, %s)"
        db_tool.print_and_try(cursor, sql, (user_id, movie_id))
    return jsonify({
        "message" : "ok"
    })

@api.route('/users/<int:user_id>/collection_movies/<int:movie_id>', methods=["DELETE"])
def delete_user_collection_movie(user_id, movie_id):
    token = other.get_request_token()
    user_id = other.verify_token(token)
    with db_tool.get_cursor() as cursor:
        sql = "DELETE FROM collection_movie WHERE user_id = %s AND movie_id = %s"
        db_tool.print_and_try(cursor, sql, (user_id, movie_id))
    return jsonify({
        "message" : "ok"
    })

@api.route('/users/<int:user_id>/movie_scores')
def get_user_movie_scores(user_id):
    token = other.get_request_token()
    user_id = other.verify_token(token)
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info INNER JOIN (SELECT movie_id, score as user_score FROM movie_score WHERE user_id = %s) tem ON movie_info.id = tem.movie_id"
        count = db_tool.print_and_try(cursor, sql, user_id)
        scores = cursor.fetchall()
    print(scores)
    return jsonify({
        "count" : count,
        "scores" : scores
    })

@api.route('/users/<int:user_id>/movie_scores/<int:movie_id>')
def get_user_movie_score(user_id, movie_id):
    token = other.get_request_token()
    user_id = other.verify_token(token)
    print(user_id)
    with db_tool.get_cursor() as cursor:
        sql = "SELECT score FROM movie_score WHERE user_id = %s AND movie_id = %s"
        count = db_tool.print_and_try(cursor, sql, (user_id, movie_id))
        score = cursor.fetchone()
    return jsonify({
        "count" : count,
        "score" : 0 if count == 0 else score.get('score')
    })

@api.route('/users/<int:user_id>/movie_scores', methods=["POST"])
def post_user_movie_score(user_id):
    token = other.get_request_token()
    user_id = other.verify_token(token)
    print(user_id)
    data = request.get_json()
    movie_id = data.get('movie_id')
    score = data.get("score")
    print(movie_id)
    with db_tool.get_cursor() as cursor:
        sql = "INSERT INTO movie_score (user_id, movie_id, score) VALUES (%s, %s, %s)"
        db_tool.print_and_try(cursor, sql, (user_id, movie_id, score))
    return jsonify({
        "message" : "ok"
    })
