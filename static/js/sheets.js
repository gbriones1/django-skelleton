$('.sheet').each(function () {
    var url = $(this).attr("use_rest")+"/"+$(this).attr("data-obj_id")+"/"
    $.getJSON(url, function (data) {
        console.log(data);
    });
});
