var storages = []
$("#new form").find('select#id_organization_storage').attr('disabled', 'disabled');
$.getJSON("/database/special-api/instorage", function (json) {
    storages = json;
    $("#new form").find('select#id_organization_storage').removeAttr('disabled');
});

$(document).on('click', 'button[data-target="#order"]', function () {
    var data = [];
    var movement_product_set = {}
    var orderform = $("#order form");
    $('table[id^="output-date"] tbody tr').each(function functionName() {
        if($(this).find(".checkthis").is(':checked')){
            var curr_set = $(this).data("movement_product_set")
            for (idx in curr_set){
                if (movement_product_set[curr_set[idx].product.id]){
                    movement_product_set[curr_set[idx].product.id] += curr_set[idx].amount
                }
                else{
                    movement_product_set[curr_set[idx].product.id] = curr_set[idx].amount
                }
            }
        }
    })
    for (product in movement_product_set){
        data.push({'product':{'id':product}, 'amount':movement_product_set[product]})
    }
    initialMultiSetData(orderform.find('input#id_order_product_set'), data);
    refreshMutliSetInputs(orderform);
});

function renderFilter(form) {
    var selectedStorage = form.find('select#id_organization_storage').val();
    form.find('table#multiSet-table tr').each(function(){
        var inStorage = storages[selectedStorage];
        if (!inStorage){
            $(this).hide();
        }
        else if (!inStorage[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('keyup change', '#multiSet-search-available', function() {
    renderFilter($(this).closest('form'))
});

function selectStorageProduct(form) {
    form.find('table#multiSet-table tr').each(function(){
        $(this).show()
    });
    var search = form.find('#multiSet-search-available').val()
    var table = form.find('#multiSet-table')
    applySearch(search, table)
    renderFilter(form)
}

$(document).on('change', '#new select#id_organization_storage', function() {
    selectStorageProduct($(this).closest('form'));
});

$(document).on('change', '#edit select#id_organization_storage', function() {
    selectStorageProduct($(this).closest('form'));
});

$('#new.modal form').each(function () {
    renderFilter($(this));
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    $("#edit form").find('select#id_organization_storage').attr('disabled', 'disabled');
    renderFilter($("#edit form"));
});

$(document).on('click', '.multiSet-add', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '.multiSet-add-all', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '.multiSet-delete', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('#multiSet-added tbody').children().length == 0){
            $(this).closest('form').find('select#id_organization_storage').removeAttr('disabled');
        }
    })
    return false;
});

$(document).on('click', '.multiSet-delete-all', function(){
    $('input.multiset').each(function functionName() {
        $(this).closest('form').find('select#id_organization_storage').removeAttr('disabled');
    })
    return false;
});

$('.modal form').submit(function () {
    $(this).find('select#id_organization_storage').removeAttr('disabled');
});
