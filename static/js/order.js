$(document).on('click', 'button[data-target="#input"]', function () {
    var data = $(this).closest('tr').data()
    var inputform = $("#input form");
    for (opIndx in data.order_product_set){
        var opData = inputform.find("input#id_movement_product_set").closest(".multiSet-container").find('#multiSet-table tbody tr[data-id='+data.order_product_set[opIndx].product.id+']').data();
        data.order_product_set[opIndx].price = opData.price
        data.order_product_set[opIndx].discount = opData.discount
        delete data.order_product_set[opIndx].id
    }
    initialMultiSetData(inputform.find("input#id_movement_product_set"), data.order_product_set);
    refreshMutliSetInputs(inputform);
    // initialFormSetData(inputform, "Product", data.products);
    // refreshFormSetInputs(inputform);
    inputform.find('input[name="order_id"]').val(data.id);
    inputform.find('select[name="organization_storage"]').val(data.organization_storage);
});

$(document).on('click', 'button[data-target="#mail"]', function () {
    var data = $(this).closest('tr').data()
    var mailform = $("#mail form");
    mailform.find('input[name="id"]').val(data.id);
});

function renderFilter(form) {
    var selectedProvider = form.find('select#id_provider').val();
    form.find('table#ProductMultiSet-table tr').each(function(){
        if (!(selectedProvider == $(this).data("provider"))){
            $(this).hide();
        }
    });
}

$(document).on('keyup change', '#ProductMultiSet-search', function() {
    renderFilter($(this).closest('form'))
});

$(document).on('change', 'select#id_provider', function() {
    var form = $(this).closest('form')
    form.find('table#ProductMultiSet-table tr').each(function(){
        $(this).show()
    });
    var search = form.find('#ProductMultiSet-search-available').val()
    var table = form.find('#ProductMultiSet-table')
    applySearch(search, table)
    renderFilter(form)
});

$('#new.modal form').each(function () {
    renderFilter($(this));
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    $("#edit form").find('select#id_provider').attr('disabled', 'disabled');
    renderFilter($("#edit form"));
});

$(document).on('click', '.ProductMultiSet-add', function(){
    $(this).closest('form').find('select#id_provider').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '.ProductMultiSet-delete', function(){
    $('#new.modal form input.multiset').each(function functionName() {
        if (!$(this).val() || JSON.parse($(this).val()).length == 0){
            $(this).closest('form').find('select#id_provider').removeAttr('disabled');
        }
    })
    return false;
});

$('.modal form').submit(function () {
    $(this).find('select#id_provider').removeAttr('disabled');
});
