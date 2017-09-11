// console.log(multiSetModelName)
// console.log(multiSetInputSetId)

function refreshMutliSetInputs(form) {
    var valueSet = []
    form.find('input.multiset').each(function () {
        var inputSet = $(this);
        var model = inputSet.data('model');
        var multiple = form.find('table#'+model+'MultiSet-table').attr('data-multiple')
        var editable = form.find('table#'+model+'MultiSet-table').attr('data-editable')
        form.find('#'+model+'MultiSet-added tbody tr').each(function () {
            var itemData = null;
            if (multiple || editable){
                itemData = $(this).data();
                if (multiple){
                    itemData["amount"] = parseInt($(this).find('.'+model+'MultiSet-amount').val())
                }
                if (editable) {
                    $(this).find('.'+model+'MultiSet-editable').each(function () {
                        itemData[$(this).attr("data-field")] = $(this).val()
                    });
                }
            }
            else{
                itemData = $(this).data('id');
            }
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

function initialMultiSetData(form, modelName, data) {
    var added = form.find('#'+modelName+'MultiSet-added')
    added.empty()
    var multiple = form.find('#'+modelName+'MultiSet-table').attr('data-multiple')
    var editable = form.find('#'+modelName+'MultiSet-table').attr('data-editable')
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
    for (index in data){
        var text = $(form.find('#'+modelName+'MultiSet-table tr[data-id="'+data[index].id+'"]').children()[0]).text()
        var row = '<tr data-id="'+data[index].id+'"><td>'+text+'</td>'
        if (multiple){
            row += '<td><input type="number" class="form-control '+modelName+'MultiSet-amount" value="'+data[index].amount+'"></td>'
        }
        if (editable){
            var fields = JSON.parse(editable);
            for (fieldName in fields){
                var fieldValue = data[index][fieldName]
                if (fields[fieldName].tag == 'input'){
                    row += '<td><input type="'+fields[fieldName].type+'" class="form-control '+multiSetModelName+'MultiSet-editable" data-field="'+fieldName+'" value="'+fieldValue+'"></td>'
                }
            }
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger '+modelName+'MultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    // refreshMutliSetInputs(form);
}

$(document).on('keyup change', '#'+multiSetModelName+'MultiSet-search-available', function() {
    var table = $(this).closest('form').find('table#'+multiSetModelName+'MultiSet-table')
    applySearch($(this).val(), table);
});

$(document).on('keyup change', '#'+multiSetModelName+'MultiSet-search-added', function() {
    var table = $(this).closest('form').find('table#'+multiSetModelName+'MultiSet-added')
    applySearch($(this).val(), table);
});

$(document).on('click', '.'+multiSetModelName+'MultiSet-add', function(){
    var val = $(this).closest('tr').attr('data-id')
    var multiple = $(this).closest('table').attr('data-multiple')
    var editable = $(this).closest('table').attr('data-editable')
    var text = $($(this).closest('tr').children()[0]).text()
    var added = $(this).closest('form').find('#'+multiSetModelName+'MultiSet-added')
    if (!added.find('thead').children().length){
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
    }
    if (added.find('tr[data-id="'+val+'"]').length){
        var amount = parseInt(added.find('tr[data-id="'+val+'"] .'+multiSetModelName+'MultiSet-amount').val()) || 0;
        if (amount){
            amount += 1
            added.find('tr[data-id="'+val+'"] .'+multiSetModelName+'MultiSet-amount').val(amount);
        }
    } else {
        var row = '<tr data-id="'+val+'"><td>'+text+'</td>'
        if (multiple){
            row += '<td><input type="number" class="form-control '+multiSetModelName+'MultiSet-amount" min="1" value="'+1+'"></td>'
        }
        if (editable){
            var fields = JSON.parse(editable);
            for (fieldName in fields){
                var fieldValue = $(this).closest('tr').attr('data-'+fieldName)
                if (fields[fieldName].tag == 'input'){
                    row += '<td><input type="'+fields[fieldName].type+'" class="form-control '+multiSetModelName+'MultiSet-editable" data-field="'+fieldName+'" value="'+fieldValue+'"></td>'
                }
            }
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger '+multiSetModelName+'MultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    // refreshMutliSetInputs($(this).closest('form'))
    return false;
});

// $(document).on('change', '.'+multiSetModelName+'MultiSet-amount', function () {
//     refreshMutliSetInputs($(this).closest('form'));
// });

$(document).on('click', '.'+multiSetModelName+'MultiSet-delete', function() {
    var thisForm = $(this).closest('form');
    $(this).closest('tr').remove();
    // refreshMutliSetInputs(thisForm);
    return false;
});

$(document).on('click', '.'+multiSetModelName+'MultiSet-add-all', function(){
    var form = $(this).closest('form');
    var added = form.find('#'+multiSetModelName+'MultiSet-added');
    var multiple = form.find('#'+multiSetModelName+'MultiSet-table').attr('data-multiple');
    var editable = form.find('#'+multiSetModelName+'MultiSet-table').attr('data-editable');
    form.find('#'+multiSetModelName+'MultiSet-table tbody tr').each(function() {
        if (this.style.display != 'none'){
            var val = $(this).attr('data-id')
            var text = $($(this).children()[0]).text()
            if (!(added.find('tr[data-id="'+val+'"]').length)) {
                var row = '<tr data-id="'+val+'"><td>'+text+'</td>'
                if (multiple){
                    row += '<td><input type="number" class="form-control '+multiSetModelName+'MultiSet-amount" min="1" value="1"></td>'
                }
                if (editable){
                    var fields = JSON.parse(editable);
                    for (fieldName in fields){
                        var fieldValue = $(this).closest('tr').attr('data-'+fieldName)
                        if (fields[fieldName].tag == 'input'){
                            row += '<td><input type="'+fields[fieldName].type+'" class="form-control '+multiSetModelName+'MultiSet-editable" data-field="'+fieldName+'" value="'+fieldValue+'"></td>'
                        }
                    }
                }
                row += '<td><button type="buttton" class="btn btn-sm btn-danger '+multiSetModelName+'MultiSet-delete"><i class="fa fa-trash"></i></button></td>'
                row += '</tr>'
                added.append(row)
            }
        }
    })
    // refreshMutliSetInputs($(this).closest('form'))
    return false;
});

$(document).on('click', '.'+multiSetModelName+'MultiSet-delete-all', function() {
    var form = $(this).closest('form');
    form.find('#'+multiSetModelName+'MultiSet-added tbody tr').remove();
    // refreshMutliSetInputs(form);
    return false;
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var form = $("#edit form");
    var value = form.find('input#'+multiSetInputSetId).val() || "[]"
    if (value){
        value = JSON.parse(value)
    }
    initialMultiSetData(form, multiSetModelName, value)
});

$('input.multiset').closest('form').submit(function () {
    var form = $(this).closest("form");
    refreshMutliSetInputs(form);
});
