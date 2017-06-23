// console.log(modelName)
// console.log(inputSetId)

function refreshInput(form) {
    var valueSet = []
    form.find('input.multiset').each(function () {
        var inputSet = $(this);
        var model = inputSet.data('model');
        var multiple = form.find('table#'+modelName+'MultiSet-table').attr('data-multiple')
        form.find('#'+model+'MultiSet-added tr').each(function () {
            var itemData = null;
            if (multiple){
                itemData = $(this).data();
                itemData["amount"] = parseInt($(this).find('.'+modelName+'MultiSet-amount').val())
            }
            else{
                itemData = $(this).data('id');
            }
            valueSet.push(itemData);
        });
        inputSet.val(JSON.stringify(valueSet));
    });
}

function applySearch(search){
    var val = search.val()
    search.closest('form').find('table#'+modelName+'MultiSet-table tr').each(function(){
        if ($($(this).children()[0]).text().match(new RegExp(val, "i"))){
            $(this).show()
        } else {
            $(this).hide()
        }
    });
}

$(document).on('keyup change', '#'+modelName+'MultiSet-search', function() {
    applySearch($(this));
});

$(document).on('click', '.'+modelName+'MultiSet-add', function(){
    var val = $(this).closest('tr').attr('data-id')
    var multiple = $(this).closest('table').attr('data-multiple')
    var text = $($(this).closest('tr').children()[0]).text()
    var added = $(this).closest('form').find('#'+modelName+'MultiSet-added')
    if (added.find('tr[data-id="'+val+'"]').length){
        var amount = parseInt(added.find('tr[data-id="'+val+'"] .'+modelName+'MultiSet-amount').val()) || 0;
        if (amount){
            amount += 1
            added.find('tr[data-id="'+val+'"] .'+modelName+'MultiSet-amount').val(amount);
        }
    } else {
        var row = '<tr data-id="'+val+'"><td>'+text+'</td>'
        if (multiple){
            row += '<td><input type="number" class="form-control '+modelName+'MultiSet-amount" min="1" value="'+1+'"></td>'
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger '+modelName+'MultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    refreshInput($(this).closest('form'))
    return false;
});

$(document).on('change', '.'+modelName+'MultiSet-amount', function () {
    refreshInput($(this).closest('form'));
});

$(document).on('click', '.'+modelName+'MultiSet-delete', function() {
    var thisForm = $(this).closest('form');
    $(this).closest('tr').remove();
    refreshInput(thisForm);
    return false;
});

$(document).on('click', '.'+modelName+'MultiSet-remove', function() {
    var amount = parseInt($($(this).closest('tr').children()[1]).text())-1
    if (amount == 0){
        $(this).closest('tr').remove()
    } else {
        $($($(this).closest('tr').children()[1]).children()[0]).text(amount)
    }
    refreshInput($(this).closest('form'))
    return false;
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var data = $(this).closest('tr').data()
    var editform = $("#edit form");
    var added = editform.find('#'+modelName+'MultiSet-added')
    added.empty()
    var elements = JSON.parse(editform.find('input#'+inputSetId).val())
    for (index in elements){
        var text = $(editform.find('#'+modelName+'MultiSet-table tr[data-id="'+elements[index].id+'"]').children()[0]).text()
        var row = '<tr data-id="'+elements[index].id+'"><td>'+text+'</td>'
        if (editform.find('#'+modelName+'MultiSet-table').attr('data-multiple')){
            row += '<td><input type="number" class="form-control '+modelName+'MultiSet-amount" value="'+elements[index].amount+'"></td>'
        }
        row += '<td><button type="buttton" class="btn btn-sm btn-danger '+modelName+'MultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        row += '</tr>'
        added.append(row)
    }
    refreshInput(editform);
});
