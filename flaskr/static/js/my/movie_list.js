$(document).ready(function () {
    var num = 0;
    var count = 20;
    var api = $("api").text();

    function get_movies() {
        $.ajax({
            type : "GET", 
            url: api + "&offset=" + num + "&count=" + count,
            success: function (data) {
                if (data.count < count) {
                    $("#load_more").hide();
                } 
                show_movie_list($("#movie_list"), data.movies);
                num += data.count;
                
            },
            error: function (data) {
                alert('error');
            }    
        });
    };

    get_movies();

    $("#load_more").click(function () {
        get_movies();
    });

});

