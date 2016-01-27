var $inputProductsSelect = $('#inputProducts');
$('#addInputProduct').click(function (argument) {
	var amount = $('#id_amount').val() || "1"
	var price = $('#id_price').val() || "1"
	var discount = getDiscount()
	var selectedProducts = $('#id_product option:selected');
	if (selectedProducts.length){
		selectedProducts.each(function(){
			if(!$inputProductsSelect.find("option[data-id='"+$(this).val()+"']").length){
				var productOpt = $(this)
				if ((parseFloat($(this).attr('price'))).toFixed(2) == parseFloat(price) && (parseFloat($(this).attr('discount'))).toFixed(2) == discount){
		            $inputProductsSelect.append($('<option>', {
		                value:productOpt.val()+":"+amount+":"+price+":"+discount,
		                "data-id":productOpt.val(),
		                text:productOpt.text()+ " x "+amount+" x $"+price+" - "+discount+"%"
		            }));
		            $('select#id_storage').attr('disabled', true);
				}
				else{
					$('#popup p.content').text("El producto "+$(this).text()+" no coincide con el precio de lista: $"+price+" y descuento del "+discount+"%. Desea cambiarle el precio y descuento a este producto?")
					$('#popup').modal('show')
					$('#popup button.ok').click(function () {
						$inputProductsSelect.append($('<option>', {
			                value:productOpt.val()+":"+amount+":"+price+":"+discount,
			                text:productOpt.text()+ " x "+amount+" x $"+price+" - "+discount+"%"
			            }));
			            $('select#id_storage').attr('disabled', true);
			            $('#popup button.ok').off();
					})
				}
	        }
	        else{
	            showNotification("Producto ya agregado", "info");
	        }
		});
	}
	else {
		showNotification("No se ha seleccionado un producto", "info");
	}
	return false;
});

$('#removeInputProduct').click(function (argument) {
    $inputProductsSelect.find('option:selected').remove();
    if ($inputProductsSelect.children().length == 0){
    	$('select#id_storage').removeAttr('disabled');
    }
    return false;
});

$('#new_input form').submit(function () {
	$('select#id_storage').removeAttr('disabled');
	var productList = {};
	$inputProductsSelect.find('option').each(function(){
		productList[$(this).val().split(":")[0]] = {amount: $(this).val().split(":")[1], price:$(this).val().split(":")[2], discount:$(this).val().split(":")[3]};
	});
	$('#new_input form input[name="inputProducts"]').val(JSON.stringify(productList));
});

$('form#multi-delete').submit(function () {
	var inputList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			inputList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="rollback"]').val($('form#multi-delete input#rollback')[0].checked)
	$('form#multi-delete input[name="input_id"]').val(JSON.stringify(inputList));
});

$('form#single-delete').submit(function () {
	$(this).find('input[name="rollback"]').val($(this).find('input#rollback')[0].checked)
});

var filterSearch = $('#id_filter_search');
filterSearch.keyup(function() {
	if ($(this).val() !== ""){
		$('#id_product option').each(function() {
            var regex = new RegExp(filterSearch.val(),"gi");
            if($(this).text().match(regex) !== null){
                $(this).prependTo($('#id_product'));
            }
		});
	}
});
var filterProvider = $('#id_provider');
filterProvider.change(function (argument) {
	$('#id_product option').each(function() {
		$(this).show();
	});
	if ($(this).val() !== ""){
		$('#id_product option').each(function() {
            if ($(this).attr("provider") != filterProvider.val()){
				$(this).hide();
            }
		});
	}
});

$('#id_price').keyup(function () {
	calculatePrice();
});
$('#id_custom_discount').keyup(function () {
	calculatePrice();
});
$('#id_price').change(function () {
	calculatePrice();
});
$('#id_custom_discount').change(function () {
	calculatePrice();
});
$("input[name=discount]:radio").change(function () {
	if ($(this).val() != -1){
		calculatePrice();
		$('#id_custom_discount').attr("disabled", true);
	}
	else{
		$('#id_custom_discount').removeAttr("disabled");
	}
});

function calculatePrice () {
	$('#id_real_price').val(($('#id_price').val()-$('#id_price').val()*getDiscount()/100).toFixed(2))
}

function getDiscount () {
	var discount = $("input[name=discount]:checked").val();
	if (discount == -1){
		discount = $('#id_custom_discount').val();
	}
	return parseFloat(discount)
}


$('table#inputs tfoot th').each( function () {
    var title = $('table#inputs thead th').eq( $(this).index() ).text();
    if (title != '' && title != "Eliminar"){
    	$(this).html( '<input type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
    else{
    	$(this).html( '<input style="display: none;" type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
} );

$('table#inputs').dataTable({
    "sScrollY": ($(window).height()-450)+"px",
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

$('table#inputs').DataTable().columns().every( function () {
    var that = this;
    $( 'input', this.footer() ).on( 'keyup change', function () {
        that.search( this.value ).draw();
    } );
});

$('#multi-email').click(function() {
	var emailListTable = $('#email-list tbody');
	var totalSum = 0;
	emailListTable.empty()
	$("table#inputs tbody tr").each(function () {
		if ($(this).find(".checkthis").is(":checked")){
			var row = $(this).clone();
			row.find(":first-child").remove();
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
		    "aoColumnDefs" : [ {
		        'bSortable' : false,
		        'aTargets' : [ 0, -1, -2 ]
		    } ],
		});
		$("#email-list_wrapper thead tr input").each(function () {
			$(this).attr("checked", true)
		});
	}
});

$("#multi-email-form").submit(function () {
	var inputProducts = [];
	$('#email-list tbody tr').each(function () {
		inputProducts.push($(this).attr("data-id"));
	});
	$('input[name="product_input_id"]').val(JSON.stringify(inputProducts))
});