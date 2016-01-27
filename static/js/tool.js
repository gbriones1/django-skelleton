$('form#multi-delete').submit(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		$('form#multi-delete input[name="code"]').val(JSON.stringify(productList));
	}
	else{
		showNotification('Debes seleccionar al menos una herramienta', 'info');
		return false;
	}
});

function getSelectedProducts () {
	var productList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			productList.push($(this).val())
		}
	});
	return productList;
}

function filterProducts (field, query) {
	$('table tbody tr').each(function(){
		value = $(this).attr('data-'+field);
		if (value.indexOf(query)+1){
			$(this).show();
		}
		else{
			$(this).hide();
		}
	});
}

$(".input-filter").keyup(function () {
	filterProducts($(this).attr("data-field"), $(this).val());
});

$(".select-filter").change(function () {
	filterProducts($(this).attr("data-field"), $(this).val());
});

$(document).on('click', 'button.edit-modal', function () {
    $('.edit-iframe').attr('data-id', $(this).attr('data-id'));
    $('.edit-iframe').attr('src', '/tool/'+$(this).attr('data-id')+'/');
});

$(document).on('click', '#edit button[type="submit"]', function (argument) {
	var form = $('.edit-iframe').contents().find('form').clone();
	form.hide();
	form.appendTo($('body'));
	form.submit();
});

$('.edit-iframe').load(function () {
	$('#edit').on('shown.bs.modal', function (e) {
		$('.edit-iframe').height($('.edit-iframe').contents().find('html').height());
	});
	$('.edit-iframe').height($('.edit-iframe').contents().find('html').height());
});

$(document).on('click', 'button.delete-modal', function () {
    $('#single-delete input[name="code"]').val('["'+$(this).attr('data-id')+'"]');
});