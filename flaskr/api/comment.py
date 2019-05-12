from flask import jsonify, request, url_for
from . import api
from ..tools import db_tool,other
import hashlib


@api.route('/comments', methods = ['POST'])
def post_comments():
    cookies = request.cookies
    token = cookies.get("token")
    print(token)
    user_id = other.verify_token(token)
    data = request.get_json()
    movie_id = data.get("movie_id")
    content = data.get("content")
    with db_tool.get_cursor() as cursor:
        sql = "INSERT INTO movie_comment (user_id, movie_id, content) VALUES (%s, %s, %s)"
        db_tool.print_and_try(cursor, sql, (user_id, movie_id, content))
    return jsonify({
        "message" : "ok"
    })

    

@api.route('/users/<int:user_id>/comments')
def get_user_comments(user_id):
    with db_tool.get_cursor() as cursor:
        sql = "SELECT movie_info.title, movie_comment.content, movie_comment.create_time FROM movie_info, movie_comment WHERE movie_comment.user_id = %s AND movie_info.id = movie_comment.movie_id"
        count = db_tool.print_and_try(cursor, sql, user_id)
        comments = cursor.fetchall()
    return jsonify({
        "count" : count,
        "comments" : comments
    })

@api.route('/movies/<int:movie_id>/comments')
def get_movie_comments(movie_id):
    args = request.args
    offset = int(args.get('offset')) if args.get('offset') else 0
    count = int(args.get('count')) if args.get('count') else 20
    with db_tool.get_cursor() as cursor:
        sql = '''SELECT user_info.nm, user_info.email, movie_comment.content, movie_comment.create_time 
                FROM user_info, movie_comment
                WHERE movie_comment.movie_id = %s AND user_info.id = movie_comment.user_id 
                ORDER BY movie_comment.create_time DESC LIMIT %s, %s
        '''
        count = db_tool.print_and_try(cursor, sql, (movie_id, offset, count))
        comments = cursor.fetchall()
    for comment in comments:
        comment['img'] = hashlib.md5(comment.pop('email').encode('utf-8')).hexdigest()
    return jsonify({
        "count" : count,
        "comments" : comments
    })



