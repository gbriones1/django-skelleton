$('button.order-modal').click(function () {
	$("#new_order form .modal-body").empty();
	var productsList = []
	$("div#"+$(this).attr("data-id")+"Diff table tbody tr.product-row").each(function () {
		productsList.push({
			code: $(this).attr("data-code"),
			name: $(this).attr("data-name"),
			description: $(this).attr("data-description"),
			amount: parseInt($(this).find(".consignment-needed").text())+parseInt($(this).find(".stock-needed").text()),
		});
	});
	$("#new_order form .modal-body").append('<div class="form-group"><label for="id_subject" class="col-sm-2 control-label">Solicitante</label><div class="col-sm-8"><input id="id_claimant" class="form-control" type="text" name="claimant"></div>');
	$("#new_order form .modal-body").append('<div class="form-group"><label for="id_subject" class="col-sm-2 control-label">Asunto</label><input id="id_subject" class="form-control" type="text" name="subject" value="Muelles Obrero S. de R.L. de C.V."></div>');
	$("#new_order form .modal-body").append('<div class="form-group"><label for="id_text" class="col-sm-2 control-label">Mensaje</label><textarea id="id_text" name="text" class="form-control" rows="4" cols="50">Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si está enderado del mismo.\nDuda o aclaración comunicarlo con almacenista a cargo.\nGracias.</textarea></div>');
	for (var productIdx in productsList){
		var product = productsList[productIdx];
		$("#new_order form .modal-body").append('<div class="form-group"><label for="'+product.code+'" class="col-sm-8 control-label">'+product.code+' - '+product.name+' - '+product.description+'</label><div class="col-sm-2"><input type="number" class="form-control" min="1" value="'+product.amount+'" name="'+product.code+'" id="'+product.code+'"></div><a class="btn btn-danger btn-sm col-sm-1 unlist-product"><span class="glyphicon glyphicon-remove"></span></a></div>');
	};
});

$(document).on('click', '.unlist-product', function (){
	$(this).closest(".form-group").remove();
});