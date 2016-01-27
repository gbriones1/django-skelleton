var $orderProductsSelect = $('#orderProducts');
$('#addOrderProduct').click(function (argument) {
	var amount = $('#new #id_amount').val() || "1";	
	var selectedProducts = $('#id_product option:selected');
	if (selectedProducts.length){
		selectedProducts.each(function(){
			if(!$orderProductsSelect.find("option[data-id='"+$(this).val()+"']").length){
	            $orderProductsSelect.append($('<option>', {
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

$('#removeOrderProduct').click(function (argument) {
    $orderProductsSelect.find('option:selected').remove();
    if ($orderProductsSelect.children().length == 0){
    	$('select#id_storage').removeAttr('disabled');
    }
    return false;
});

$('#new form').submit(function () {
	$('select#id_storage').removeAttr('disabled');
	var productList = {};
	$orderProductsSelect.find('option').each(function(){
		productList[$(this).val().split(":")[0]] = $(this).val().split(":")[1];
	});
	$('#new form input[name="orderProducts"]').val(JSON.stringify(productList));
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

$('.product-input').each(function () {
	$(this).find(".discount").keyup(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
	$(this).find(".discount").change(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
	$(this).find(".price").keyup(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
	$(this).find(".price").change(function () {
		calculateRealPrice($(this).closest(".product-input"));
	});
});

function calculateRealPrice (section) {
	var discount = section.find(".discount").val();
	var price = section.find('.price').val();
	section.find('.real_price').val((price-price*discount/100).toFixed(2));
}

$(document).on('click', '.unlist-product', function (){
	$(this).closest(".form-group").remove();
});

$(document).on('keyup', 'input[name="invoice_number"]', function (){
	sessionStorage.setItem("LastInvoiceNumber", $(this).val());
});

$(document).on('click', '.new-input', function (){
	var id = $(this).attr("data-id")
	if (sessionStorage.getItem("LastInvoiceNumber")){
		$('#input'+id).find('input[name="invoice_number"]').val(sessionStorage.getItem("LastInvoiceNumber"));
	}
	else{
		$('#input'+id).find('input[name="invoice_number"]').val("");
	}
});

$('table#orders tfoot th').each( function () {
    var title = $('table#orders thead th').eq( $(this).index() ).text();
    if (title != '' && title != "Acciones"){
    	$(this).html( '<input type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
    else{
    	$(this).html( '<input style="display: none;" type="text" placeholder="Buscar '+title+'" class="form-control" />' );
    }
} );

var table = $('table#orders').dataTable({
    "sScrollY": ($(window).height()-485)+"px",
    "sScrollX": "100%",
    "bScrollCollapse": true,
    "bPaginate": false,
    "sDom": '<"top">rt<"bottom"lp><"clear">',
    'bAutoWidth': false , 
    "aoColumnDefs" : [ {
        'bSortable' : false,
        'aTargets' : [ -1 ],
    }, {
    	"sWidth": "300px", 
        'aTargets' : [ -1 ],
    }],
    "aaSorting": [[0,'asc']]
});

$('table#orders').DataTable().columns().every( function () {
    var that = this;
    $( 'input', this.footer() ).on( 'keyup change', function () {
        that.search( this.value ).draw();
    } );
});


$(document).on('submit', 'form.input-form', function (){
	var price = $(this).find('input[name="hidden_price"]').val();
	var discount = $(this).find('input[name="hidden_discount"]').val();
	var new_price = $(this).find('input[name="price"]').val();
	var new_discount = $(this).find('input[name="discount"]').val();
	var form = $(this);
	if (price != new_price || discount != new_discount){
		$('#popup p.content').text("El precio y descuento ingresados no coinciden con los del producto: Precio de lista: $"+price+" y descuento del "+discount+"% actuales. Desea cambiarle el precio y descuento a este producto?")
		$('#popup').modal('show')
		$('#popup button.ok').click(function (e) {
	        e.preventDefault();
			form.find('button[type="submit"]').attr("disabled", true);
	        form[0].submit();
	        $('#popup button.ok').off();
		});
		$(this).find('button[type="submit"]').attr("disabled", false);
		return false;
	}
});