$(document).on('click', 'button[data-target="#order"]', function () {
    var data = $(this).closest('tr').data()
    var orderform = $("#order form");
    var added = orderform.find('#ProductMultiSet-added')
    added.empty()
    for (index in data.products){
        var text = $(orderform.find('#ProductMultiSet-table tr[data-id="'+data.products[index].id+'"]').children()[0]).text()
        var row = '<tr data-id="'+data.products[index].id+'"><td>'+text+'</td>'
        if (orderform.find('#ProductMultiSet-multiplier').length){
            row += '<td><input type="number" class="form-control ProductMultiSet-amount" value="'+data.products[index].amount+'"></td>'
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger ProductMultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    refreshInput(orderform);
    orderform.find('select[name="organization_storage"]').val(data.organization_storage);
});
