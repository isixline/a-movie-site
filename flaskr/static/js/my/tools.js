function show_movie_list($movie_list, movies){
    var $movie_item = $movie_list.children(":first")
    $movie_item.hide();
    $.each(movies, function(index, movie){
        var $movie_item_clone = $movie_item.clone();
        $("img", $movie_item_clone).attr("src","https://image.tmdb.org/t/p/w185_and_h278_bestv2"+ movie.poster_path);
        $(".title", $movie_item_clone).text(movie.title);
        $("p", $movie_item_clone).html(movie.release_date + "<br/>" + movie.overview.substring(0, 100) + "...");
        if("user_score" in movie){
            set_star($(".rating", $movie_item_clone), movie.user_score)
        }
        else{
            set_star($(".rating", $movie_item_clone), movie.score)
        }
        $movie_item_clone.attr("onclick", "window.open('/movie/"+movie.id+"')")
        $movie_item_clone.show();
        $movie_item_clone.appendTo($movie_list);       
    });
}

function show_movie_grid($movie_grid, movies){
    var $movie_item = $movie_grid.children(":first")
    $movie_item.hide();
    $.each(movies, function(index, movie){
        var $movie_item_clone = $movie_item.clone();
        $("img", $movie_item_clone).attr("src","https://image.tmdb.org/t/p/w185_and_h278_bestv2"+ movie.poster_path);
        $("p", $movie_item_clone).text(movie.title.substring(0, 12));
        $("a", $movie_item_clone).attr("href", "/movie/"+movie.id)
        set_star($(".rating", $movie_item_clone), movie.score)
        $movie_item_clone.show();
        $movie_item_clone.appendTo($movie_grid);       
    });
}


function show_comment_list($comment_list, comments){
    var $comment_item = $comment_list.children(":first")
    $comment_item.hide();
    $.each(comments, function(index, comment){
        var $comment_item_clone = $comment_item.clone();
        $("img", $comment_item_clone).attr("src", "https://secure.gravatar.com/avatar/" + comment.img +"?d=identicon")
        if("nm" in comment){
            $("h5", $comment_item_clone).text(comment.nm)
        }
        else{
            $("h5", $comment_item_clone).text(comment.title)
        }
        $("h6", $comment_item_clone).text(comment.create_time)
        $("p", $comment_item_clone).text(comment.content)
        $comment_item_clone.show();
        $comment_item_clone.appendTo($comment_list);       
    });
}

function show_movlist_list($movlist_list, movlists){
    var $movlist_item = $movlist_list.children(":first")
    $movlist_item.hide();
    $.each(movlists, function(index, movlist){
        var $movlist_item_clone = $movlist_item.clone();
        $heading = $(".panel-heading", $movlist_item_clone)
        $("a", $heading).html(movlist.title + "  (" + movlist.count+ ")" + "<p>" + movlist.create_time + "</p>")
        $("a", $heading).attr("href", "#"+movlist.id)


        $collapse = $(".panel-collapse", $movlist_item_clone) 
        $collapse.attr("id", movlist.id)
        
        $body = $(".panel-body", $collapse)
        
        show_movie_list($(".row", $body), movlist.movies)

        $movlist_item_clone.show();
        $movlist_item_clone.appendTo($movlist_list);       
    });
}

function set_star($star_list, score){
    var int_score = parseInt(score)
    $star_list.children("i").removeClass()
    for (var i = 0;i < int_score; i++){
        var $star = $star_list.children().eq(i)
        $star.addClass("fa fa-star")
    }
    for(var i = int_score; i < 10 ;i++){
        var $star = $star_list.children().eq(i)
        $star.addClass("fa fa-star-o")
    }

    $("span", $star_list).text(score)
}