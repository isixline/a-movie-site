CREATE TABLE user_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    nm VARCHAR(255) NOT NULL,
    pwd VARCHAR(255) NOT NULL
);

CREATE TABLE movie_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tmdb_id INT UNIQUE,
    imdb_id VARCHAR(255),
    title VARCHAR(255),
    original_title VARCHAR(255),
    release_date DATE,
    overview TEXT,
    poster_path VARCHAR(255),
    backdrop_path VARCHAR(255),
    score FLOAT(3,1) DEFAULT 0,
    vote_count INT DEFAULT 0,
    review_count INT DEFAULT 0
);



CREATE TABLE movlist(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE
);



CREATE TABLE movie_comment( 
    movie_id INT,
    user_id Int,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    content TEXT,
    FOREIGN KEY (movie_id) REFERENCES movie_info(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE
);

CREATE TABLE movie_score(
    movie_id INT,
    user_id INT,
    score INT,
    PRIMARY KEY(movie_id,user_id),
    FOREIGN KEY (movie_id) REFERENCES movie_info(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE 
);

CREATE TABLE collection_movie(
    user_id INT,
    movie_id INT,
    add_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(user_id, movie_id),
    FOREIGN KEY (movie_id) REFERENCES movie_info(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE
);


CREATE TABLE movlist_movie(
    movlist_id INT,
    movie_id INT,
N    PRIMARY KEY(movie_id,movlist_id),
    FOREIGN KEY (movlist_id) REFERENCES movlist(id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES movie_info(id) ON DELETE CASCADE

);





