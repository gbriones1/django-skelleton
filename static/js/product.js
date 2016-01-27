$('button[data-target="#new_input"]').click(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		var $formBody = $('#new_input .modal-body .fields-area');
		$formBody.empty();
		for (var productIdx in productList){
			var fieldStr = '<div class="form-group"><label class="col-sm-8 control-label">';
			fieldStr += getProductName(productList[productIdx]);
			fieldStr += '</label><div class="col-sm-4">';
			fieldStr += '<input type="number" class="form-control" name="'+productList[productIdx]+'" value="1" />';
			fieldStr += '</div></div>';
			$formBody.append(fieldStr);
		}
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info')
	}
});

$('#new_input form').submit(function () {
	var inputProducts = {};
	$('#new_input form .modal-body input').each(function () {
		inputProducts[$(this).attr("name")] = $(this).val();
	});
	$('#new_input form input[name="inputProducts"]').val(JSON.stringify(inputProducts));
});

$('button[data-target="#new_output"]').click(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		var $formBody = $('#new_output .modal-body .fields-area');
		$formBody.empty();
		for (var productIdx in productList){
			var fieldStr = '<div class="form-group"><label class="col-sm-8 control-label">';
			fieldStr += getProductName(productList[productIdx]);
			fieldStr += '</label><div class="col-sm-4">';
			fieldStr += '<input type="number" class="form-control" name="'+productList[productIdx]+'" value="1" />';
			fieldStr += '</div></div>';
			$formBody.append(fieldStr);
		}
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info')
	}
});

$('#new_output form').submit(function () {
	var outputProducts = {};
	$('#new_output form .modal-body input').each(function () {
		outputProducts[$(this).attr("name")] = $(this).val();
	});
	$('#new_output form input[name="outputProducts"]').val(JSON.stringify(outputProducts));
});

$('button[data-target="#new_lending"]').click(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		var $formBody = $('#new_lending .modal-body');
		$formBody.empty();
		for (var productIdx in productList){
			var fieldStr = '<div class="form-group"><label class="col-sm-8 control-label">';
			fieldStr += getProductName(productList[productIdx]);
			fieldStr += '</label><div class="col-sm-4">';
			fieldStr += '<input type="number" class="form-control" name="'+productList[productIdx]+'" value="1" />';
			fieldStr += '</div></div>';
			$formBody.append(fieldStr);
		}
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info')
	}
});

$('form#multi-delete').submit(function () {
	var productList = getSelectedProducts();
	if (productList.length){
		$('form#multi-delete input[name="code"]').val(JSON.stringify(productList));
	}
	else{
		showNotification('Debes seleccionar al menos un producto', 'info');
		return false;
	}
});

$('input[name="storage"]').each(function () {
	var storage = $(this).val();
	switch (storage){
		case "C":
			$(this).closest('form').find('[name="in_stock"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="in_used"]').closest(".form-group").hide()
			break;
		case "S":
			$(this).closest('form').find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="consignment_tobe"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="in_used"]').closest(".form-group").hide()
			break;
		case "U":
			$(this).closest('form').find('[name="in_stock"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).closest('form').find('[name="consignment_tobe"]').closest(".form-group").hide()
			break;
	}
});

$('input[name="discount"]').keyup(function () {
	calculateRealPrice($('#new form'));
});
$('input[name="discount"]').change(function () {
	calculateRealPrice($('#new form'));
});
$('input[name="price"]').keyup(function () {
	calculateRealPrice($('#new form'));
});
$('input[name="price"]').change(function () {
	calculateRealPrice($('#new form'));
});

function calculateRealPrice (form) {
	var discount = form.find("input[name=discount]").val();
	var price = form.find('#id_price').val();
	form.find('#id_real_price').val((price-price*discount/100).toFixed(2));
}

function getProductName (code) {
	return $('tr#'+code+' td.product-name').text()
}

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
	$('table#products tbody tr').each(function(){
		var value = $(this).attr('data-'+field);
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

$(".multi-select-filter").change(function () {
	var query = $(this).val()
	var field = $(this).attr("data-field")
	$('table#products tbody tr').each(function(){
		var allValue = $(this).attr('data-'+field);
		var found = false;
		if (allValue){
			for (valueIdx in allValue.split(":")){
				if (allValue.split(":")[valueIdx].indexOf(query)+1){
					found = true;
				}
			}
		}
		if (found){
			$(this).show();
		}
		else{
			$(this).hide();
		}
	});
});

$(document).on('click', 'button.edit-modal', function () {
    $('.edit-iframe').attr('data-id', $(this).attr('data-id'));
    var storage = location.search.split("storage=")[1]
    if (storage){
    	$('.edit-iframe').attr('src', '/product/'+$(this).attr('data-id')+'/?storage='+storage[0]);
    }
    else{
    	$('.edit-iframe').attr('src', '/product/'+$(this).attr('data-id'));
    }
});

$(document).on('click', '#edit button[type="submit"]', function (argument) {
	var form = $('.edit-iframe').contents().find('form').clone();
	form.hide();
	form.appendTo($('body'));
	form.submit();
});

$('.edit-iframe').load(function () {
	switch ($('#new input[name="storage"]').val()){
		case "C":
			$(this).contents().find('[name="in_stock"]').closest(".form-group").hide()
			$(this).contents().find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).contents().find('[name="in_used"]').closest(".form-group").hide()
			break;
		case "S":
			$(this).contents().find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).contents().find('[name="consignment_tobe"]').closest(".form-group").hide()
			$(this).contents().find('[name="in_used"]').closest(".form-group").hide()
			break;
		case "U":
			$(this).contents().find('[name="in_stock"]').closest(".form-group").hide()
			$(this).contents().find('[name="stock_tobe"]').closest(".form-group").hide()
			$(this).contents().find('[name="in_consignment"]').closest(".form-group").hide()
			$(this).contents().find('[name="consignment_tobe"]').closest(".form-group").hide()
			break;
	}
	calculateRealPrice($('.edit-iframe').contents().find('form'));
	$('.edit-iframe').contents().find('input[name="discount"]').keyup(function () {
		calculateRealPrice($('.edit-iframe').contents().find('form'));
	});
	$('.edit-iframe').contents().find('input[name="discount"]').change(function () {
		calculateRealPrice($('.edit-iframe').contents().find('form'));
	});
	$('.edit-iframe').contents().find('input[name="price"]').keyup(function () {
		calculateRealPrice($('.edit-iframe').contents().find('form'));
	});
	$('.edit-iframe').contents().find('input[name="price"]').change(function () {
		calculateRealPrice($('.edit-iframe').contents().find('form'));
	});
	$('#edit').on('shown.bs.modal', function (e) {
		$('.edit-iframe').height($('.edit-iframe').contents().find('html').height()+20);
	});
	$('.edit-iframe').height($('.edit-iframe').contents().find('html').height());
});

$(document).on('click', 'button.delete-modal', function () {
    $('#single-delete input[name="code"]').val('["'+$(this).attr('data-id')+'"]');
});

$('table#products tfoot th').each( function () {
    var title = $('table#products thead th').eq( $(this).index() ).text();
    if (title != '' && title != "Actualizar" && title != "Eliminar"){
    	$(this).html( '<input type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
    else{
    	$(this).html( '<input style="display: none;" type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
} );

$('table#products').dataTable({
    "sScrollY": ($(window).height()-320)+"px",
    "sScrollX": "98%",
    "bScrollCollapse": true,
    "bPaginate": false,
    "sDom": '<"top">rt<"bottom"lp><"clear">',
    "aoColumnDefs" : [ {
        'bSortable' : false,
        'aTargets' : [ 0, -1, -2 ]
    } ],
    "aaSorting": [[1,'asc']]
});

$('table#products').DataTable().columns().every( function () {
    var that = this;
    $( 'input', this.footer() ).on( 'keyup change', function () {
        that.search( this.value ).draw();
    } );
} );


$(window).bind('beforeunload', function(){
	var temporaryInput = {}
	$('#new form input').each(function() {
		temporaryInput[$(this).attr('name')] = $(this).val();
	});
	sessionStorage.setItem("NewProduct", JSON.stringify(temporaryInput));
});

if (sessionStorage.getItem("NewProduct")){
	var temporaryInput = JSON.parse(sessionStorage.getItem("NewProduct"));
	$('#new form input').each(function() {
		$(this).val(temporaryInput[$(this).attr("name")]);
	});
}

function calculateRealPercentage () {
	var emailListTable = $('#email-list tbody');
	var percentage = $('input[name="percentage"]:checked').val().slice(-1)
	var totalSum1 = 0;
	var totalSum2 = 0;
	var totalSum3 = 0;
	emailListTable.find('tr').each(function () {
		var amount = parseInt($(this).find('td.amount input').val());
		var p1 = parseFloat($(this).find('td.unit-price').attr("data-p1"));
		var p2 = parseFloat($(this).find('td.unit-price').attr("data-p2"));
		var p3 = parseFloat($(this).find('td.unit-price').attr("data-p3"));
		if (percentage == 1){
			$(this).find('td.unit-price').text("$"+p1.toFixed(2));
			$(this).find('td.total-price').text("$"+p1.toFixed(2)*amount);
		}
		else if (percentage == 2){
			$(this).find('td.unit-price').text("$"+p2.toFixed(2));
			$(this).find('td.total-price').text("$"+p2.toFixed(2)*amount);
		}
		else if (percentage == 3){
			$(this).find('td.unit-price').text("$"+p3.toFixed(2));
			$(this).find('td.total-price').text("$"+p3.toFixed(2)*amount);
		}
		totalSum1 += p1*amount;
		totalSum2 += p2*amount;
		totalSum3 += p3*amount;
	});
	$("p.percentage1").text("$"+totalSum1.toFixed(2));
	$("p.percentage2").text("$"+totalSum2.toFixed(2));
	$("p.percentage3").text("$"+totalSum3.toFixed(2));
}

$(document).on('change', 'td.amount input', function () {
	calculateRealPercentage()
});

$(document).on('change', 'input[name="percentage"]', function () {
	calculateRealPercentage()
});

$('#pricing-btn').click(function() {
	var emailListTable = $('#email-list tbody');
	emailListTable.empty()
	$("table#products tbody tr").each(function () {
		if ($(this).find(".checkthis").is(":checked")){
			var row = $(this).clone();
			var p1 = parseFloat(row.attr("data-percentage-one"));
			var p2 = parseFloat(row.attr("data-percentage-two"));
			var p3 = parseFloat(row.attr("data-percentage-three"));
			row.find(":first-child").remove();
			row.find(":last-child").remove();
			row.find(":last-child").remove();
			row.find(":last-child").remove();
			row.find(":last-child").remove();
			row.find(":last-child").remove();
			row.find(":last-child").remove();
			row.append('<td class="amount"><input type="number" class="form-control" name="amount'+row.attr('id')+'"" value="1" min="1"></td>');
			row.append('<td class="unit-price" data-p1="'+p1+'", data-p2="'+p2+'" data-p3="'+p3+'">$'+p1.toFixed(2)+'</td>');
			row.append('<td class="total-price">$'+p1.toFixed(2)+'</td>');
			emailListTable.append(row);
		}
	});
	calculateRealPercentage();
	var emailList = $('table#email-list')
	if (!emailList.hasClass("dataTable")){
		emailList.dataTable({
		    "sScrollX": "98%",
		    "bScrollCollapse": true,
		    "bPaginate": false,
		    "sDom": '<"top">rt<"bottom"lp><"clear">',
		    "aoColumnDefs" : [ {
		        'bSortable' : false,
		        'aTargets' : [ 0, -1, -2, -3 ]
		    } ],
		});
		$("#email-list_wrapper thead tr input").each(function () {
			$(this).attr("checked", true)
		});
	}
});