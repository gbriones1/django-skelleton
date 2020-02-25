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

function getFormData(form){
    var unindexed_array = form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

(function ($) {
    $.fn.serialize = function (options) {
        return $.param(this.serializeArray(options));
    };

    $.fn.serializeArray = function (options) {
        var o = $.extend({
            checkboxesAsBools: false
        }, options || {});

        var rselectTextarea = /select|textarea/i;
        var rinput = /text|hidden|password|search|number/i;

        return this.map(function () {
            return this.elements ? $.makeArray(this.elements) : this;
        })
        .filter(function () {
            return this.name && !this.disabled &&
                (this.checked
                || (o.checkboxesAsBools && this.type === 'checkbox')
                || rselectTextarea.test(this.nodeName)
                || rinput.test(this.type));
            })
            .map(function (i, elem) {
                var val = $(this).val();
                return val == null ?
                null :
                $.isArray(val) ?
                $.map(val, function (val, i) {
                    return { name: elem.name, value: val };
                }) :
                {
                    name: elem.name,
                    value: (o.checkboxesAsBools && this.type === 'checkbox') ?
                        (this.checked ? true : false) :
                        val
                };
            }).get();
    };
})(jQuery);

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
function createAlert(text, level) {
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
        class:"alert alert-"+level+" alert-dismissible fade show",
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
    createAlert($(this).attr("data-message"), $(this).attr("data-level"));
});

var messages = {};
$('.global-messages').children().each(function () {
    messages[$(this).attr("data-action")] = $(this).attr("data-parameter");
});

for (var action in messages){
    if (action.startsWith("update-")){
        var name = action.substring(7);
        if (messages[action] > sessionStorage.getItem(action)){
            sessionStorage.removeItem(name)
        }
        sessionStorage.setItem(action, messages[action])
    }
}

$('#update_userpass form').submit(function (argument) {
    $('input[name="next"]').val(location.pathname);
});

$('li.filter-menu').click(function(){return false});

$('.table-fixed-height').height($(window).height()-320);
