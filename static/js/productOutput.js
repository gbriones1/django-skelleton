var selectedStorage = $('select#id_storage').val();
function switchStorage (storage) {
	switch (storage){
		case "C":
			$('select#id_product_consignment').closest('.form-group').show();
			$('select#id_product_stock').closest('.form-group').hide();
			$('select#id_product_used').closest('.form-group').hide();
			selectedStorage = storage;
			break;
		case "S":
			$('select#id_product_consignment').closest('.form-group').hide();
			$('select#id_product_stock').closest('.form-group').show();
			$('select#id_product_used').closest('.form-group').hide();
			selectedStorage = storage;
			break;
		case "U":
			$('select#id_product_consignment').closest('.form-group').hide();
			$('select#id_product_stock').closest('.form-group').hide();
			$('select#id_product_used').closest('.form-group').show();
			selectedStorage = storage;
			break;
		default:
			$('select#id_product_consignment').closest('.form-group').hide();
			$('select#id_product_stock').closest('.form-group').hide();
			$('select#id_product_used').closest('.form-group').hide();
			selectedStorage = storage;
			break;
	}
}
switchStorage($('select#id_storage').val());
$('select#id_storage').change(function () {
	switchStorage($(this).val());
});

var $outputProductsSelect = $('#outputProducts');
$('#addOutputProduct').click(function (argument) {
	var amount = $('#id_amount').val() || "1"
	var selectedProducts = []
	switch (selectedStorage){
		case "C":
			selectedProducts = $('#id_product_consignment option:selected');
			break;
		case "S":
			selectedProducts = $('#id_product_stock option:selected');
			break;
		case "U":
			selectedProducts = $('#id_product_used option:selected');
			break;
		default:
			break;
	}
	if (selectedProducts.length){
		selectedProducts.each(function(){
			if(!$outputProductsSelect.find("option[data-id='"+$(this).val()+"']").length){
	            $outputProductsSelect.append($('<option>', {
	                value:$(this).val()+":"+amount,
		            "data-id":$(this).val(),
	                text:$(this).text()+ " x "+amount
	            }));
	            $('select#id_storage').attr('disabled', true);
	        }
	        else{
	            showNotification("Producto ya agregado", "info");
	        }
		})
	}
	else {
		showNotification("No se ha seleccionado un producto", "info");
	}
	return false;
});

$('#removeOutputProduct').click(function (argument) {
    $outputProductsSelect.find('option:selected').remove();
    if ($outputProductsSelect.children().length == 0){
    	$('select#id_storage').removeAttr('disabled');
    }
    return false;
});

$('#new_output form').submit(function () {
	$('select#id_storage').removeAttr('disabled');
	var productList = {};
	$outputProductsSelect.find('option').each(function(){
		productList[$(this).val().split(":")[0]] = $(this).val().split(":")[1];
	});
	$('#new_output form input[name="outputProducts"]').val(JSON.stringify(productList));
});

$('form#multi-delete').submit(function () {
	var outputList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			outputList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="rollback"]').val($('form#multi-delete input#rollback')[0].checked)
	$('form#multi-delete input[name="output_id"]').val(JSON.stringify(outputList));
});

$('form#single-delete').submit(function () {
	$(this).find('input[name="rollback"]').val($(this).find('input#rollback')[0].checked)
});

var filterSearch = $('#id_filter_search');
filterSearch.keyup(function() {
	if ($(this).val() !== ""){
		$('#id_product_consignment option').each(function() {
            var regex = new RegExp(filterSearch.val(),"gi");
            if($(this).text().match(regex) !== null){
                $(this).prependTo($('#id_product_consignment'));
            }
		});
		$('#id_product_stock option').each(function() {
            var regex = new RegExp(filterSearch.val(),"gi");
            if($(this).text().match(regex) !== null){
                $(this).prependTo($('#id_product_stock'));
            }
		});
		$('#id_product_used option').each(function() {
            var regex = new RegExp(filterSearch.val(),"gi");
            if($(this).text().match(regex) !== null){
                $(this).prependTo($('#id_product_used'));
            }
		});
	}
});
var filterProvider = $('#id_provider');
filterProvider.change(function (argument) {
	$('#id_product_consignment option').each(function() {
		$(this).show();
	});
	$('#id_product_stock option').each(function() {
		$(this).show();
	});
	$('#id_product_used option').each(function() {
		$(this).show();
	});
	if ($(this).val() !== ""){
		$('#id_product_consignment option').each(function() {
            if ($(this).attr("provider") != filterProvider.val()){
				$(this).hide();
            }
		});
		$('#id_product_stock option').each(function() {
            if ($(this).attr("provider") != filterProvider.val()){
				$(this).hide();
            }
		});
		$('#id_product_used option').each(function() {
            if ($(this).attr("provider") != filterProvider.val()){
				$(this).hide();
            }
		});
	}
});

$('table#outputs tfoot th').each( function () {
    var title = $('table#outputs thead th').eq( $(this).index() ).text();
    if (title != '' && title != "Enviar" && title != "Eliminar" && title != "Editar"){
    	$(this).html( '<input type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
    else{
    	$(this).html( '<input style="display: none;" type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
} );

$('table#outputs').dataTable({
    "sScrollY": ($(window).height()-450)+"px",
    "sScrollX": "98%",
    "bScrollCollapse": true,
    "bPaginate": false,
    "sDom": '<"top">rt<"bottom"lp><"clear">',
    "aoColumnDefs" : [ {
        'bSortable' : false,
        'aTargets' : [ 0, -1, -2, -3 ]
    } ],
    "aaSorting": [[1,'asc']]
});

$('table#outputs').DataTable().columns().every( function () {
    var that = this;
    $( 'input', this.footer() ).on( 'keyup change', function () {
        that.search( this.value ).draw();
    } );
});



$('#multi-email').click(function() {
	var emailListTable = $('#email-list tbody');
	var totalSum = 0;
	emailListTable.empty()
	$("table#outputs tbody tr").each(function () {
		if ($(this).find(".checkthis").is(":checked")){
			var row = $(this).clone();
			row.find(":first-child").remove();
			row.find(":last-child").remove();
            row.find(":last-child").remove();
            row.find(":last-child").remove();
			emailListTable.append(row);
			totalSum += parseFloat(row.find('.product-total').text().substring(1))
		}
	});
	$(".total-sum").text("$"+totalSum.toFixed(2));
	var emailList = $('table#email-list')
	if (!emailList.hasClass("dataTable")){
		emailList.dataTable({
		    "sScrollX": "98%",
		    "bScrollCollapse": true,
		    "bPaginate": false,
		    "sDom": '<"top">rt<"bottom"lp><"clear">',
		});
		$("#email-list_wrapper thead tr input").each(function () {
			$(this).attr("checked", true)
		});
	}
});

$("#multi-email-form").submit(function () {
	var outputProducts = [];
	$('#email-list tbody tr').each(function () {
		outputProducts.push($(this).attr("data-id"));
	});
	$('input[name="product_output_id"]').val(JSON.stringify(outputProducts))
});

$('#order-btn').click(function () {
	$("#new_order form .modal-body").empty();
	var productsList = []
	$("table#outputs tbody tr").each(function () {
		if ($(this).find(".checkthis").is(":checked")){
			productsList.push({
				code: $(this).attr("data-product-code"),
				name: $(this).attr("data-product-name"),
				description: $(this).attr("data-product-description"),
				amount: parseInt($(this).find(".needed").text().substring(2)),
				storage: $(this).attr("data-storage"),
				organization: $(this).attr("data-organization"),
				in_storage: $(this).attr("data-in-storage"),
				storage_tobe: $(this).attr("data-storage-tobe"),
			});
		}
	});
	$("#new_order form .modal-body").append('<div class="form-group"><label for="id_subject" class="col-sm-2 control-label">Solicitante</label><div class="col-sm-8"><input id="id_claimant" class="form-control" type="text" name="claimant"></div>');
	$("#new_order form .modal-body").append('<div class="form-group"><label for="id_subject" class="col-sm-2 control-label">Asunto</label><input id="id_subject" class="form-control" type="text" name="subject" value="Muelles Obrero S. de R.L. de C.V."></div>');
	$("#new_order form .modal-body").append('<div class="form-group"><label for="id_text" class="col-sm-2 control-label">Mensaje</label><textarea id="id_text" name="text" class="form-control" rows="4" cols="50">Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si está enderado del mismo.\nDuda o aclaración comunicarlo con almacenista a cargo.\nGracias.</textarea></div>');
	for (var productIdx in productsList){
		var product = productsList[productIdx];
		$("#new_order form .modal-body").append('<input type="hidden" value="'+product.storage+'" name="storage'+product.code+'"><input type="hidden" value="'+product.organization+'" name="organization'+product.code+'"><div class="form-group"><label for="'+product.code+'" class="col-sm-8 control-label">'+product.code+' - '+product.name+' - '+product.description+' Existentes: '+product.in_storage+' Stock: '+product.storage_tobe+'</label><div class="col-sm-2"><input type="number" class="form-control" min="1" value="'+product.amount+'" name="'+product.code+'" id="'+product.code+'"></div><a class="btn btn-danger btn-sm col-sm-1 unlist-product"><span class="glyphicon glyphicon-remove"></span></a></div>');
	};
});

$(document).on('click', '.unlist-product', function (){
	$(this).closest(".form-group").remove();
});