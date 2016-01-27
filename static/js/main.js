webshims.setOptions('waitReady', false);
webshims.setOptions('forms-ext', {types: 'date'});
webshims.polyfill('forms forms-ext');

$('div.form-group input').each(function(){
    if ($(this).attr("type")!="checkbox" && $(this).attr("type")!="radio"){
        $(this).addClass("form-control")
    }
});
$('div.form-group select').each(function(){
	$(this).addClass("form-control")
});
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


$('#update_userpass form').submit(function (argument) {
    $('input[name="next"]').val(location.pathname);
});

$('li.filter-menu').click(function(){return false});

$('.table-fixed-height').height($(window).height()-320);