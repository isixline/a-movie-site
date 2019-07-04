from flask import jsonify, request, url_for
from . import api
from ..tools import db_tool,other
from math import sqrt
from .movie import get_movies
from .movlist import get_movlists

def get_user_movie_data():
    data = {}
    with db_tool.get_cursor() as cursor:
        sql = "SELECT id FROM user_info"
        db_tool.print_and_try(cursor, sql)
        persons = cursor.fetchall()
    with db_tool.get_cursor() as cursor:
        sql = "SELECT movie_id, score FROM movie_score WHERE user_id = %s"
        for person in persons:
            data[person["id"]] = {}
            db_tool.print_and_try(cursor, sql, person["id"])
            movie_scores = cursor.fetchall()
            for movie_score in movie_scores:
                data[person["id"]][movie_score["movie_id"]] = movie_score["score"]
                
    return data

def transformdata(data):
    newdata = {}
    for person in data:
        for movie in data[person]:
            newdata.setdefault(movie, {})
            newdata[movie][person] = data[person][movie]
    return newdata

def sim_pearson(data, person1, person2):
    
    commonmovies = [] 
    for movie in data[person1]: 
        if movie in data[person2]: 
            commonmovies.append(movie) 

    n = float(len(commonmovies))
    if n == 0:
        return 0

    sum1 = sum([data[person1][movie] for movie in commonmovies])
    sum2 = sum([data[person2][movie] for movie in commonmovies])

    sum12 = sum([data[person1][movie] * data[person2][movie] for movie in commonmovies])

    sum1Sq = sum([pow(data[person1][movie], 2) for movie in commonmovies])
    sum2Sq = sum([pow(data[person2][movie], 2) for movie in commonmovies])

    num = sum12 - sum1 * sum2 / n

    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:  return 0

    return num / den


def topmatches(data, givenperson, count=20, simscore=sim_pearson):
    usersscores = [(simscore(data, givenperson, other), other) for other in data if other != givenperson]
    usersscores.sort(key=None, reverse=True)

    return usersscores[:count]


def recommendItems(data, givenperson, count=20, simscore=sim_pearson):
    
    itemsimsum = {}
    itemsum = {}

    for otheruser in data:
        if otheruser == givenperson:   continue
        sim = simscore(data, givenperson, otheruser)
        if sim <= 0:   continue

        for itemmovie in data[otheruser]:
            if itemmovie not in data[givenperson]:
                itemsum.setdefault(itemmovie, 0)
                itemsimsum.setdefault(itemmovie, 0)
                itemsum[itemmovie] += sim * data[otheruser][itemmovie]
                itemsimsum[itemmovie] += sim

    rankings = [(itemsum[itemmovie] / itemsimsum[itemmovie], itemmovie) for itemmovie in itemsum]
    rankings.sort(key=None, reverse=True)
    return rankings[:count]


@api.route('/users/recommend_movies')
def get_user_recommend_movie():
    token = other.get_request_token()
    if (token is None):
        return get_movies()
    user_id = other.verify_token(token)
    data = get_user_movie_data()
    rankings = recommendItems(data, user_id)[:19]
    movie_ids = []
    for ranking in rankings:
        movie_ids.append(ranking[1])
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info WHERE id IN " + str(tuple(movie_ids))
        db_tool.print_and_try(cursor, sql)
        movies = cursor.fetchall()
    return jsonify({
        "count" : 19,
        "movies" : movies
    })

@api.route('/movies/<int:movie_id>/recommend_movies')
def get_movie_recommend_movie(movie_id):
    data = get_user_movie_data()
    moviedata = transformdata(data)
    results = topmatches(moviedata, movie_id)[:4]
    movie_ids = []
    for result in results:
        movie_ids.append(result[1])
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movie_info WHERE id IN " + str(tuple(movie_ids))
        db_tool.print_and_try(cursor, sql)
        movies = cursor.fetchall()
    return jsonify({
        "count" : 4,
        "movies" : movies
    })

@api.route('/users/recommend_movlists')
def get_user_recommend_movlist():
    token = other.get_request_token()
    if (token is None):
        return get_movlists()
    user_id = other.verify_token(token)
    data = get_user_movie_data()
    results = topmatches(data, user_id)[:10]
    user_ids = []
    for result in results:
        user_ids.append(result[1])
    with db_tool.get_cursor() as cursor:
        sql = "SELECT * FROM movlist WHERE user_id IN " + str(tuple(user_ids)) + "ORDER BY create_time DESC"
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
    




