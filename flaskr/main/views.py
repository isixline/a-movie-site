from flask import render_template, request
from . import main

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/user')
def user():
    return render_template('user.html')

@main.route('/movie/<int:id>')
def movie(id):
    return render_template('movie.html', movie_id=id)


@main.route('/top_movie')
def top_movie():
    return render_template('movie_list.html', title="高分榜", api="/api/movies?order_by=score")

@main.route('/hot_movie')
def hot_movie():
    return render_template('movie_list.html', title="热评榜", api="/api/movies?order_by=vote_count")

@main.route('/lately_movie')
def lately_movie():
    return render_template('movie_list.html', title="最近上映", api="/api/movies?order_by=release_date")

@main.route('/recommend_movie')
def recommend_movie():
    return render_template('movie_list.html', title="推荐电影", api="/api/users/recommend_movies?order_by=release_date")

@main.route('/recommend_movlist')
def recommend_movlist():
    return render_template('recommend_movlist.html')


@main.route('/movie/search')
def search_movie():
    args = request.args
    q = args.get('q')
    return render_template('movie_list.html', title="搜索电影： %s" % q, api="/api/movies/search?q=%s" % q)

@main.route('/movlist/<int:id>')
def movlist(id):
    return render_template('movie_list.html', title="影单：%d" % id, api="/api/movlist/%d?order_by=add_time" % id)