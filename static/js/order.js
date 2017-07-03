$(document).on('click', 'button[data-target="#input"]', function () {
    var data = $(this).closest('tr').data()
    var inputform = $("#input form");
    var added = inputform.find('#ProductMultiSet-added')
    added.empty()
    for (index in data.products){
        var text = $(inputform.find('#ProductMultiSet-table tr[data-id="'+data.products[index].id+'"]').children()[0]).text()
        var row = '<tr data-id="'+data.products[index].id+'"><td>'+text+'</td>'
        if (inputform.find('#ProductMultiSet-table').attr('data-multiple')){
            row += '<td><input type="number" class="form-control ProductMultiSet-amount" value="'+data.products[index].amount+'"></td>'
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger ProductMultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    refreshMutliSetInputs(inputform);
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
