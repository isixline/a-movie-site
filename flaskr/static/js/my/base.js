$(document).ready(function () {
    if ($.cookie('nm')) {
        $("#account").text($.cookie('nm'));
        $("#account").attr("href", "/user");
        $("#account").attr("onclick", "window.location.replace('/user');")
        

    }
    

    var $sigin = $("#sigin");
    $sigin.submit(function () {
        email = $("input[name='email']", $sigin).val()
        pwd = $("input[name='pwd']", $sigin).val()
        get_token(email, pwd);
        return false;
    });

    var $sigup = $("#signup");
    $sigup.submit(function () {
        nm = $("input[name='nm']", $sigup).val()
        email = $("input[name='email']", $sigup).val()
        pwd = $("input[name='pwd']", $sigup).val()
        $.ajax({
            type: "POST",
            url: "/api/users",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "nm" : nm,
                "email": email,
                'pwd': pwd
            }),
            success: function (data) {
                get_token(email, pwd);
            }
        });
        return false;
    });

    function get_token(email, pwd){
        $.ajax({
            type: "POST",
            url: "/api/tokens",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "email": email,
                'pwd': pwd
            }),
            success: function (data) {
                $.cookie('id', data.id, {
                    path: '/'
                });
                $.cookie('nm', data.nm, {
                    path: '/'
                });
                $.cookie('token', data.token, {
                    path: '/'
                });
                window.location.reload();
            },
            error: function (data) {
                toastr.error('获取失败！')
            }
        });
    }

});