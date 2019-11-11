// console.log(multiSetModelName)
// console.log(multiSetInputSetId)

function refreshMutliSetInputs(form) {
    var valueSet = []
    form.find('input.multiset').each(function () {
        var inputSet = $(this);
        var multiple = inputSet.closest('.multiSet-container').find('table#multiSet-table').attr('data-multiple')
        var editable = inputSet.closest('.multiSet-container').find('table#multiSet-table').attr('data-editable')
        inputSet.closest('.multiSet-container').find('#multiSet-added tbody tr').each(function (key, value) {
            var itemData = null;
            if (multiple || editable){
                itemData = $(this).data();
                if (multiple){
                    itemData["amount"] = parseInt($(this).find('.multiSet-amount').val())
                }
                if (editable) {
                    $(this).find('.multiSet-editable').each(function () {
                        itemData[$(this).attr("data-field")] = $(this).val()
                    });
                }
            }
            else{
                itemData = $(this).data('id');
            }
            var form = inputSet.closest('form');
            $('<input>').attr({
                type: 'hidden',
                id: 'id_'+inputSet.attr('name')+'['+key+']',
                name: inputSet.attr('name')+'['+key+']',
                value: JSON.stringify(itemData)
            }).appendTo('form');
            valueSet.push(itemData);
        });
        inputSet.val(JSON.stringify(valueSet));
    });
}

function applySearch(search, table){
    table.find('tr').each(function(){
        if ($($(this).children()[0]).text().match(new RegExp(search, "i"))){
            $(this).show()
        } else {
            $(this).hide()
        }
    });
}

function initialMultiSetData(input, data) {
    var div = input.closest('.multiSet-container')
    // var modelName = input.attr('data-model')
    var reference = input.data("related")
    var added = div.find('#multiSet-added')
    added.empty()
    var multiple = div.find('#multiSet-table').attr('data-multiple')
    var editable = div.find('#multiSet-table').attr('data-editable')
    var thead = "<thead><tr><th>Nombre</td>"
    if (multiple){
        thead += "<th>Cant</th>"
    }
    if (editable){
        var fields = JSON.parse(editable);
        for (fieldName in fields){
            thead += "<th>"+fieldName+"</th>"
        }
    }
    thead += "</tr></thead>"
    added.append(thead)
    var body = $('<tbody>');
    for (index in data){
        var text = $(div.find('#multiSet-table tr[data-id="'+data[index][reference].id+'"]').children()[0]).text()
        var row = '<tr data-id="'+data[index].id+'" data-'+reference+'="'+data[index][reference].id+'"><td>'+text+'</td>'
        if (multiple){
            row += '<td><input type="number" class="form-control multiSet-amount" value="'+data[index].amount+'"></td>'
        }
        if (editable){
            var fields = JSON.parse(editable);
            for (fieldName in fields){
                var fieldValue = data[index][fieldName]
                if (fields[fieldName].tag == 'input'){
                    row += '<td><input type="'+fields[fieldName].type+'" class="form-control multiSet-editable" data-field="'+fieldName+'" value="'+fieldValue+'"></td>'
                }
            }
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger multiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        body.append(row)
    }
    added.append(body);
    // refreshMutliSetInputs(form);
}

$(document).on('keyup change', '#multiSet-search-available', function() {
    var table = $(this).closest('.multiSet-container').find('table#multiSet-table')
    applySearch($(this).val(), table);
});

$(document).on('keyup change', '#multiSet-search-added', function() {
    var table = $(this).closest('.multiSet-container').find('table#multiSet-added')
    applySearch($(this).val(), table);
});

$(document).on('click', '.multiSet-add', function(){
    var reference = $(this).closest('.multiSet-container').find('input.multiset').data("related")
    var val = $(this).closest('tr').attr('data-id')
    var multiple = $(this).closest('table').attr('data-multiple')
    var editable = $(this).closest('table').attr('data-editable')
    var text = $($(this).closest('tr').children()[0]).text()
    var added_thead = $(this).closest('.multiSet-container').find('#multiSet-added thead')
    var added = $(this).closest('.multiSet-container').find('#multiSet-added tbody')
    if (added_thead.children().length == 0){
        var thead = "<tr><th>Nombre</td>"
        if (multiple){
            thead += "<th>Cant</th>"
        }
        if (editable){
            var fields = JSON.parse(editable);
            for (fieldName in fields){
                thead += "<th>"+fieldName+"</th>"
            }
        }
        thead += "</tr>"
        added_thead.append(thead)
    }
    if (added.find('tr[data-'+reference+'="'+val+'"]').length){
        var amount = parseInt(added.find('tr[data-'+reference+'="'+val+'"] .multiSet-amount').val()) || 0;
        if (amount){
            amount += 1
            added.find('tr[data-'+reference+'="'+val+'"] .multiSet-amount').val(amount);
        }
    } else {
        var row = '<tr data-'+reference+'="'+val+'"><td>'+text+'</td>'
        if (multiple){
            row += '<td><input type="number" class="form-control multiSet-amount" min="1" value="'+1+'"></td>'
        }
        if (editable){
            var fields = JSON.parse(editable);
            for (fieldName in fields){
                var fieldValue = $(this).closest('tr').attr('data-'+fieldName)
                if (fields[fieldName].tag == 'input'){
                    row += '<td><input type="'+fields[fieldName].type+'" class="form-control multiSet-editable" data-field="'+fieldName+'" value="'+fieldValue+'"></td>'
                }
            }
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger multiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    // refreshMutliSetInputs($(this).closest('form'))
    return false;
});

$(document).on('click', '.multiSet-delete', function() {
    $(this).closest('tr').remove();
    // refreshMutliSetInputs(thisForm);
    return false;
});

$(document).on('click', '.multiSet-add-all', function(){
    var div = $(this).closest('.multiSet-container');
    var added = div.find('#multiSet-added tbody');
    var multiple = div.find('#multiSet-table').attr('data-multiple');
    var editable = div.find('#multiSet-table').attr('data-editable');
    var reference = div.find('input.multiset').data("related");
    div.find('#multiSet-table tbody tr').each(function() {
        if (this.style.display != 'none'){
            var val = $(this).attr('data-id')
            var text = $($(this).children()[0]).text()
            if (!(added.find('tr[data-'+reference+'="'+val+'"]').length)) {
                var row = '<tr data-'+reference+'="'+val+'"><td>'+text+'</td>'
                if (multiple){
                    row += '<td><input type="number" class="form-control multiSet-amount" min="1" value="1"></td>'
                }
                if (editable){
                    var fields = JSON.parse(editable);
                    for (fieldName in fields){
                        var fieldValue = $(this).closest('tr').attr('data-'+fieldName)
                        if (fields[fieldName].tag == 'input'){
                            row += '<td><input type="'+fields[fieldName].type+'" class="form-control multiSet-editable" data-field="'+fieldName+'" value="'+fieldValue+'"></td>'
                        }
                    }
                }
                row += '<td><button type="buttton" class="btn btn-sm btn-danger multiSet-delete"><i class="fa fa-trash"></i></button></td>'
                row += '</tr>'
                added.append(row)
            }
        }
    })
    // refreshMutliSetInputs($(this).closest('form'))
    return false;
});

$(document).on('click', '.multiSet-delete-all', function() {
    // var div = $(this).closest('div');
    $(this).closest('div').find('#multiSet-added tbody tr').remove();
    // refreshMutliSetInputs(form);
    return false;
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var form = $("#edit form");
    form.find('input.multiset').each(function() {
        var value = $(this).val() || "[]"
        if (value){
            value = JSON.parse(value)
        }
        initialMultiSetData($(this), value)
    })
});

$('input.multiset').closest('form').submit(function () {
    var form = $(this).closest("form");
    refreshMutliSetInputs(form);
});
