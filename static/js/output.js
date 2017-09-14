var storages = []
$("#new form").find('select#id_organization_storage').attr('disabled', 'disabled');
$.getJSON("/database/special-api/instorage", function (json) {
    storages = json;
    $("#new form").find('select#id_organization_storage').removeAttr('disabled');
});

$(document).on('click', 'button[data-target="#order"]', function () {
    var data = $(this).closest('tr').data()
    var orderform = $("#order form");
    var added = orderform.find('#ProductMultiSet-added')
    added.empty()
    for (index in data.products){
        var text = $(orderform.find('#ProductMultiSet-table tr[data-id="'+data.products[index].id+'"]').children()[0]).text()
        var row = '<tr data-id="'+data.products[index].id+'"><td>'+text+'</td>'
        if (orderform.find('#ProductMultiSet-table').attr('data-multiple')){
            row += '<td><input type="number" class="form-control ProductMultiSet-amount" value="'+data.products[index].amount+'"></td>'
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger ProductMultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    refreshMutliSetInputs(orderform);
    orderform.find('select[name="organization_storage"]').val(data.organization_storage);
});

function renderFilter(form) {
    var selectedStorage = form.find('select#id_organization_storage').val();
    form.find('table#ProductMultiSet-table tr').each(function(){
        var inStorage = storages[selectedStorage];
        if (!inStorage){
            $(this).hide();
        }
        else if (!inStorage[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('keyup change', '#ProductMultiSet-search-available', function() {
    renderFilter($(this).closest('form'))
});

$(document).on('change', 'select#id_organization_storage', function() {
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
    $("#edit form").find('select#id_organization_storage').attr('disabled', 'disabled');
    renderFilter($("#edit form"));
});

$(document).on('click', '.ProductMultiSet-add', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '.ProductMultiSet-add-all', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '.ProductMultiSet-delete', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('#ProductMultiSet-added tbody').children().length == 0){
            $(this).closest('form').find('select#id_organization_storage').removeAttr('disabled');
        }
    })
    return false;
});

$(document).on('click', '.ProductMultiSet-delete-all', function(){
    $('input.multiset').each(function functionName() {
        $(this).closest('form').find('select#id_organization_storage').removeAttr('disabled');
    })
    return false;
});

$('.modal form').submit(function () {
    $(this).find('select#id_organization_storage').removeAttr('disabled');
});
