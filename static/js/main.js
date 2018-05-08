webshims.setOptions('waitReady', false);
webshims.setOptions('forms-ext', {types: 'date'});
webshims.polyfill('forms forms-ext');

function getParameterByName(name, url) {
    if (!url) {
      url = window.location.href;
    }
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

var urlParams;
(window.onpopstate = function () {
    var match,
        pl     = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
        query  = window.location.search.substring(1);

    urlParams = {};
    while (match = search.exec(query))
       urlParams[decode(match[1])] = decode(match[2]);
})();

$('div.form-group input').each(function(){
    if ($(this).attr("type")!="checkbox" && $(this).attr("type")!="radio"){
        $(this).addClass("form-control")
    }
});
$('div.form-group select').each(function(){
	$(this).addClass("form-control")
});
var date__gte = urlParams["date__gte"];
var date__lt = urlParams["date__lt"];
if (date__lt){
    console.log(date__lt);
    $('.filter_form input#id_date__lt').val(date__lt);
}
if (date__gte){
    $('.filter_form input#id_date__gte').val(date__gte);
}


$(document).on('click', "table #checkall", function () {
    if ($(this).is(':checked')) {
        $("table input[type=checkbox]").each(function () {
            $(this).prop("checked", true);
        });

    } else {
        $("table input[type=checkbox]").each(function () {
            $(this).prop("checked", false);
        });
    }
});
$("[data-toggle=tooltip]").tooltip();

$(document).on('click', 'button[type="submit"]', function () {
    $(this).attr('disabled', true);
    $(this).closest('form').submit();
})

var notifications = $('.notifications')
function showNotification(text, level) {
	var icon = '<strong></strong>'
	switch(level){
		case "success":
			icon = '<strong><i class="fa fa-check"></i></strong> '
			break;
		case "warning":
			icon = '<strong><i class="fa fa-warning"></i></strong> '
			break;
		case "info":
			icon = '<strong><i class="fa fa-info"></i></strong> '
			break;
		case "danger":
			icon = '<strong><i class="fa fa-times"></i></strong> '
			break;
	}
	var notice = $('<div>', {
        class:"alert alert-"+level+" alert-dismissible fade in",
    }).append($('<button>', {
    	type:"button",
    	class:"close",
    	"data-dismiss":"alert",
    	"aria-label":"Close"
    }).append($('<span>', {
    	"aria-hidden":"true",
    	text:"x"
    }))).append(icon+text);
    notifications.append(notice)
    // setTimeout(function() {
    // 	notice.alert('close');
    // }, 5000);
}
$('.messages').children().each(function () {
    showNotification($(this).attr("data-message"), $(this).attr("data-level"));
});

var messages = {};
$('.global-messages').children().each(function () {
    messages[$(this).attr("data-action")] = $(this).attr("data-parameter");
});


$('#update_userpass form').submit(function (argument) {
    $('input[name="next"]').val(location.pathname);
});

$('li.filter-menu').click(function(){return false});

$('.table-fixed-height').height($(window).height()-320);
