UPDATE movie_info a JOIN (SELECT movie_id, AVG(score) as avg_score, COUNT(score) as count_score FROM movie_score GROUP BY movie_id) b
ON a.id = b.movie_id
SET a.score = b.avg_score, a.vote_count = b.count_score