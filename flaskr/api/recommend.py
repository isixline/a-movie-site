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
    '''
    物品之间的相似度 与 用户之间的相似度 求解 一样。故只需要将用户换成物品即可
    '''
    newdata = {}
    for person in data:
        for movie in data[person]:
            # 初始化
            newdata.setdefault(movie, {})
            # 物品与用户对调
            newdata[movie][person] = data[person][movie]  # 字典可以直接写[key]，就表示插入key值了。非常简便
    return newdata

def sim_distance(data, person1, person2):
    '''欧氏距离求相似度，距离越大，越相似'''
    commonmovies = [movie for movie in data[person1] if movie in data[person2]]
    if len(commonmovies) == 0: return 0
    # 平方和
    sumSq = sum([pow(data[person1][movie] - data[person2][movie], 2) for movie in commonmovies])
    # 使最终结果是，越相似，距离越大。所以将上面距离取倒数即可
    sim = 1 / (1 + sqrt(sumSq))
    return sim


def sim_pearson(data, person1, person2):
    '''
    计算上面格式的数据 里的  两个用户 相似度.
    基于用户过滤思路：找出两个用户看过的相同电影的评分，从而进行按pearson公式求值。那些非公共电影不列入求相似度值范围。
    基于物品过滤思路：找过两部电影相同的观影人给出的评分，从而按pearson公式求值
    返回：评分的相似度，[-1,1]范围，0最不相关，1，-1为正负相关，等于1时，表示两个用户完全一致评分
    这里的data格式很重要，这里计算相似度是严格按照上面data格式所算。
    此字典套字典格式，跟博客计算单词个数 存储格式一样
    '''
    # 计算pearson系数，先要收集两个用户公共电影名单
    # commonmovies = [ movie for movie in data[person1] if movie in data[person2]] 分解步骤为如下：
    commonmovies = []  # 改成列表呢
    for movie in data[person1]:  # data[person1]是字典，默认第一个元素 in （字典）是指 key.所以这句话是指 对data[person1]字典里遍历每一个key=movie
        if movie in data[person2]:  # data[person2]也是字典，表示该字典有key是movie.
            commonmovies.append(movie)  # commonmovie是  两个用户的公共电影名的列表

    # 看过的公共电影个数
    n = float(len(commonmovies))
    if n == 0:
        return 0

    '''下面正是计算pearson系数公式 '''
    # 分布对两个用户的公共电影movie分数总和
    sum1 = sum([data[person1][movie] for movie in commonmovies])
    sum2 = sum([data[person2][movie] for movie in commonmovies])

    # 计算乘积之和
    sum12 = sum([data[person1][movie] * data[person2][movie] for movie in commonmovies])

    # 计算平方和
    sum1Sq = sum([pow(data[person1][movie], 2) for movie in commonmovies])
    sum2Sq = sum([pow(data[person2][movie], 2) for movie in commonmovies])

    # 计算分子
    num = sum12 - sum1 * sum2 / n
    # 分母
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:  return 0

    return num / den


def topmatches(data, givenperson, count=20, simscore=sim_pearson):
    '''
    用户匹配推荐：给定一个用户，返回对他口味最匹配的其他用户
    物品匹配： 给定一个物品，返回相近物品
    输入参数：对person进行默认推荐count=5个用户（基于用户过滤），或是返回5部电影物品（基于物品过滤），相似度计算用pearson计算
    '''
    # 建立最终结果列表
    usersscores = [(simscore(data, givenperson, other), other) for other in data if other != givenperson]
    # 对列表排序
    usersscores.sort(key=None, reverse=True)

    return usersscores[:count]

def calSimilarItems(data, num=10):
    # 以物品为中心，对偏好矩阵转置
    moviedata = transformdata(data)
    ItemAllMatches = {}
    for movie in moviedata:
        ItemAllMatches.setdefault(movie, [])
        # 对每个电影 都求它的匹配电影集,求电影之间的距离用pearson距离
        ItemAllMatches[movie] = topmatches(moviedata, movie, num, simscore=sim_pearson)
    return ItemAllMatches


def getrecommendations(data, targetperson, moviesAllsimilarity):
    '''
    输入movieAllSimilarity就是上面calsimilarItems已经计算好的所有物品之间的相似度数据集：
     '''
    # 获得所有物品之间的相似数据集
    scoresum = {}
    simsum = {}
    # 遍历所有看过的电影
    for watchedmovie in data[targetperson]:
        rating = data[targetperson][watchedmovie]
        # 遍历与当前电影相近的电影
        for (similarity, newmovie) in moviesAllsimilarity[watchedmovie]:  # 取一对元组
            # 已经对当前物品评价过，则忽略
            if newmovie in data[targetperson]: continue

            scoresum.setdefault(newmovie, 0)
            simsum.setdefault(newmovie, 0)
            # 全部相似度求和
            simsum[newmovie] += similarity
            # 评价值与相似度加权之和
            scoresum[newmovie] += rating * similarity

    rankings = [(score / simsum[newmovie], newmovie) for newmovie, score in scoresum.items()]
    rankings.sort(key=None, reverse=True)
    return rankings

def recommendItems(data, givenperson, count=20, simscore=sim_pearson):
    '''
    物品推荐：给定一个用户person,默认返回count=5物品
    要两个for,对用户，物品 都进行 遍历
    '''
    # 所有变量尽量用字典，凡是列表能表示的字典都能表示，那何不用字典
    itemsimsum = {}
    # 存给定用户没看过的电影的其他用户评分加权
    itemsum = {}

    # 遍历每个用户，然后遍历该用户每个电影
    for otheruser in data:
        # 不要和自己比较
        if otheruser == givenperson:   continue
        # 忽略相似度=0或小于0情况
        sim = simscore(data, givenperson, otheruser)
        if sim <= 0:   continue

        for itemmovie in data[otheruser]:
            # 只对用户没看过的电影进行推荐，参考了其他用户的评价值（协同物品过滤是参考了历史物品相似度值）
            if itemmovie not in data[givenperson]:
                # 一定要初始化字典：初始化itemsum与itemsimsum
                itemsum.setdefault(itemmovie, 0)
                itemsimsum.setdefault(itemmovie, 0)
                # 用户相似度*评价值
                itemsum[itemmovie] += sim * data[otheruser][itemmovie]
                itemsimsum[itemmovie] += sim

                # 最终结果列表，列表包含一元组（item,分数）
    rankings = [(itemsum[itemmovie] / itemsimsum[itemmovie], itemmovie) for itemmovie in itemsum]
    # 结果排序
    rankings.sort(key=None, reverse=True)
    return rankings[:count]



#data = get_user_movie_data()
#moviedata = transformdata(data)
#itemsAllsim = calSimilarItems(data) 

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
    




