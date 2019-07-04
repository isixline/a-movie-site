$(document).ready(function () {
    movie_id = $("movie_id").text();
    var $comment_form = $("#comment_form");
    var $movlist_from = $("#movlist_form");

    var $movlist_list = $("#movlist_list", $movlist_from)
    var $movlist_item = $movlist_list.children(":first").clone()
    $movlist_list.empty()

    var $star_list = $(".rating", $("#star_dialog"))
    

    var num = 0;
    var count = 20;
    var is_collected = false;
    var score = 0;

    get_movie();
    get_comments();
    get_recommend_movie();

    if ($.cookie('token')) {
        $("#movlist_b").click(function () {
            $.ajax({
                type: "GET",
                url: "/api/users/" + $.cookie('id') + "/movlists",
                contentType: "application/json",
                dataType: "json",
                success: function (data) {
                    movlists = data.movlists;
                    $movlist_list.empty();
                    $.each(movlists, function (index, movlist) {
                        var is_check = false
                        $.each(movlist.movies, function (index, movie) {
                            if (movie.movie_id == movie_id) {
                                is_check = true
                            }
                        })
                        var $movlist_item_clone = $movlist_item.clone()
                        $("input", $movlist_item_clone).attr("value", movlist.id);
                        $("input", $movlist_item_clone).attr("id", movlist.id);
                        $("input", $movlist_item_clone).attr("checked", is_check);
                        $("label", $movlist_item_clone).attr("for", movlist.id);
                        $("label", $movlist_item_clone).text(movlist.title)
                        $movlist_item_clone.appendTo($movlist_list);
                    });

                    $("#movlist_dialog").modal('show')
                },
                error: function (data) {
                    toastr.error('获取失败！')
                }
            });
        })

        init_collection_b()
        $("#collection_b").click(function () {
            if (is_collected) {
                $.ajax({
                    type: "DELETE",
                    url: "/api/users/" + $.cookie('id') + "/collection_movies/" + movie_id,
                    success: function (data) {
                        $("i", $("#collection_b")).removeClass("fa-heart")
                        $("i", $("#collection_b")).addClass("fa-heart-o")
                        is_collected = false
                    },
                    error: function (data) {
                        toastr.error('取消收藏失败！')
                    }
                });
            } else {
                $.ajax({
                    type: "POST",
                    url: "/api/users/" + $.cookie('id') + "/collection_movies",
                    contentType: "application/json",
                    dataType: "json",
                    data: JSON.stringify({
                        "movie_id": movie_id
                    }),
                    success: function (data) {
                        $("i", $("#collection_b")).removeClass("fa-heart-o")
                        $("i", $("#collection_b")).addClass("fa-heart")
                        is_collected = true
                    },
                    error: function (data) {
                        toastr.error('收藏失败！')
                    }
                });
            }
        })

        init_star_b()
        $("#star_b").click(function () {
            $("#star_dialog").modal('show')
        })


        $("#comment_b").click(function () {
            $("#comment_dialog").modal('show')
        })



    } else {
        $("#movlist_b").click(function () {
            $("#account").click();
        })

        $("#collection_b").click(function () {
            $("#account").click();
        })

        $("#star_b").click(function () {
            $("#account").click();
        })

        $("#comment_b").click(function () {
            $("#account").click();
        })


    }



    $("#load_more").click(function () {
        get_comments();
    });



    function get_movie() {
        $.ajax({
            type: "GET",
            url: "/api/movies/" + movie_id,
            success: function (data) {
                movie = data.movie;
                $("#movie_poster").attr("src", "https://image.tmdb.org/t/p/w185_and_h278_bestv2/" + movie.poster_path);
                $("#movie_background").css("background-image", "url(https://image.tmdb.org/t/p/original/" + movie.backdrop_path + ")");
                $("#movie_title").text(movie.title);
                $("#movie_score").text(movie.score + "/10 (" + movie.vote_count + ")");
                $("#movie_overview").text(movie.overview)
                $("#movie_release_date").text(movie.release_date);
                $("#movie_original_title").text(movie.original_title);
                $("#movie_imdb_id").text(movie.imdb_id)
                $("#movie_imdb_id").attr("href", "https://www.imdb.com/title/" + movie.imdb_id)
                $("#movie_tmdb_id").text(movie.tmdb_id)
                $("#movie_tmdb_id").attr("href", "https://www.themoviedb.org/movie/" + movie.tmdb_id)
                
            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });
    };



    function get_comments() {
        $.ajax({
            type: "GET",
            url: "/api/movies/" + movie_id + "/comments?offset=" + num + "&count=" + count,
            success: function (data) {
                if (data.count < count) {
                    $("#load_more").hide();
                }
                show_comment_list($("#comment_list"),data.comments);
                num += data.count;

            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });

    };




    $comment_form.submit(function () {
        content_text = $("textarea[name='content_text']", $comment_form).val()
        $.ajax({
            type: "POST",
            url: "/api/comments",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "movie_id": movie_id,
                "content": content_text
            }),
            success: function (data) {
                toastr.success('提交成功！')
                window.location.reload();
            },
            error: function (data) {
                toastr.error('提交失败！')
            }
        });

        return false;
    });

    $movlist_from.submit(function () {
        var vals = [];
        $('input:checkbox:checked', $movlist_from).each(function (index, item) {
            vals.push($(this).val());
        });
        $.each(vals, function (index, val) {
            $.ajax({
                type: "POST",
                url: "/api/movlists/" + val + "/movies",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({
                    "movie_id": movie_id
                }),
                success: function (data) {},
                error: function (data) {
                    toastr.error('提交失败！')
                }
            });
        })
        $("#movlist_dialog").modal('hide')
        toastr.success('提交成功！')
        return false;
    });


    function init_collection_b() {
        $.ajax({
            type: "GET",
            url: "/api/users/" + $.cookie('id') + "/collection_movies/" + movie_id,
            success: function (data) {
                if (data.count != 0) {
                    $("i", $("#collection_b")).removeClass("fa-heart-o")
                    $("i", $("#collection_b")).addClass("fa-heart")
                    is_collected = true
                }
            },
            error: function (data) {
                toastr.error('init_获取失败！')
            }
        });
    }

    function init_star_b() {
        $.ajax({
            type: "GET",
            url: "/api/users/" + $.cookie('id') + "/movie_scores/" + movie_id,
            success: function (data) {
                if (data.count != 0) {
                    $("i", $("#star_b")).removeClass("fa-star-o")
                    $("i", $("#star_b")).addClass("fa-star")

                    set_star($(".rating"), data.score)
                    $("#star_submit").css({ "display": "none" });

                }
                else {
                    $star_list.children(".fa").click(function(){
                        score = $(this).prevAll().length + 1
                        set_star($star_list, score)
                    })
                    
                    $("#star_submit").click(function(){
                        $.ajax({
                            type: "POST",
                            url: "/api/users/" + $.cookie('id') + "/movie_scores",
                            contentType: "application/json",
                            dataType: "json",
                            data: JSON.stringify({
                                "movie_id": movie_id,
                                "score" : score
                            }),
                            success: function (data) {
                                toastr.success('提交成功！')
                                window.location.reload();


                            },
                            error: function (data) {
                                toastr.error('提交失败！')
                            }
                        });
                    })
                }
            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });
        
    };


    function get_recommend_movie(){
        $.ajax({
            type : "GET", 
            url:  "/api/movies/" + movie_id + "/recommend_movies",
            success: function (data) {
                show_movie_grid($("#movie_grid"), data.movies);
            },
            error: function (data) {
                toastr.error('获取失败！')
            }    
        });
    }

});