$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: "/api/users/recommend_movlists",
        success: function (data) {
            show_movlist_list($($("#movlist_list")), data.movlists);
        },
        error: function (data) {
            toastr.error('获取失败！')
        }
    });




});