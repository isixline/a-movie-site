$(document).ready(function () {
    var $collection_b = $("#collection_b");
    var $movlist_b = $("#movlist_b");
    var $score_b = $("#score_b");
    var $comment_b = $("#comment_b");

    var $collection_div = $("#collection_div");
    var $movlist_div = $("#movlist_div");
    var $score_div = $("#score_div");
    var $comment_div = $("#comment_div");

    var collection_data
    var movlist_data
    var score_data
    var comment_data



    function get_collection_movies() {
        $.ajax({
            type: "GET",
            url: "/api/users/" + $.cookie('id') + "/collection_movies",
            success: function (data) {
                collection_data = data
                $("#collection_h").text("收藏电影（" + collection_data.count + ")")
        show_movie_list($("#movie_list", $collection_div), collection_data.movies);
            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });
    };

    function get_movlist_list() {
        $.ajax({
            type: "GET",
            url: "/api/users/" + $.cookie('id') + "/movlists",
            success: function (data) {
                movlist_data = data
                $("#movlist_h").text("影单（" + movlist_data.count + ")")
                show_movlist_list($($("#movlist_list"), $movlist_div), movlist_data.movlists);
            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });
    }

    function get_score_list() {
        $.ajax({
            type: "GET",
            url: "/api/users/" + $.cookie('id') + "/movie_scores",
            success: function (data) {
                score_data = data
                $("#score_h").text("我的评分（" + score_data.count + ")")
                show_movie_list($($("#score_list"), $score_div), score_data.scores);
            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });
    }

    function get_comment_list() {
        $.ajax({
            type: "GET",
            url: "/api/users/" + $.cookie('id') + "/comments",
            success: function (data) {
                comment_data = data
                $("#comment_h").text("我的评论（" + comment_data.count + ")")
                show_comment_list($($("#comment_list"), $comment_div), comment_data.comments);
            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });
    }



    $collection_b.click(function () {
        change_button($collection_b)
        if (!collection_data) {
            get_collection_movies()
        }
        change_div($collection_div)
    });

    $movlist_b.click(function () {
        change_button($movlist_b)
        if (!movlist_data) {
            get_movlist_list()
        }
        change_div($movlist_div)

    });

    $score_b.click(function () {
        change_button($score_b)
        if (!score_data) {
            get_score_list()
        }
        change_div($score_div)

    });

    $comment_b.click(function () {
        change_button($comment_b)
        if (!comment_data) {
            get_comment_list()
        }
        change_div($comment_div)

    });


    function change_button(b) {
        $collection_b.attr("disabled", false)
        $movlist_b.attr("disabled", false)
        $score_b.attr("disabled", false)
        $comment_b.attr("disabled", false)
        b.attr("disabled", true)
    }

    function change_div(d) {
        $collection_div.css("display", "none")
        $movlist_div.css("display", "none")
        $score_div.css("display", "none")
        $comment_div.css("display", "none")
        d.css("display", "inline")
    }


    $("#add_movlist_a").click(function () {
        $("#add_movlist_dialog").modal('show')
    })

    var $add_movlist_form = $("#add_movlist_form")
    $add_movlist_form.submit(function () {
        movlist_title = $("input[name='movlist_title']", $add_movlist_form).val()
        $.ajax({
            type: "POST",
            url: "/api/movlists",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "title": movlist_title
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


    

});