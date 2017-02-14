console.log(modelName)
console.log(inputSetId)

function refreshInput(form) {
    var valueSet = []
    var inputSet = form.find('input#'+inputSetId)
    form.find('#'+modelName+'MultiSet-added tr').each(function () {
        var itemData = $(this).data();
        itemData["amount"] = parseInt($($(this).children()[1]).text());
        valueSet.push(itemData);
    });
    inputSet.val(JSON.stringify(valueSet));
}

$(document).on('keyup change', '#'+modelName+'MultiSet-search', function() {
    var val = $(this).val()
    $(this).closest('form').find('table#'+modelName+'MultiSet-table tr').each(function(){
        if ($($(this).children()[0]).text().match(new RegExp(val, "i"))){
            $(this).show()
        } else {
            $(this).hide()
        }
    });
});

$(document).on('click', '.'+modelName+'MultiSet-add', function(){
    var val = $(this).closest('tr').attr('data-id')
    var text = $($(this).closest('tr').children()[0]).text()
    var added = $(this).closest('form').find('#'+modelName+'MultiSet-added')
    if (added.find('tr[data-id="'+val+'"]').length){
        var amount = parseInt($(added.find('tr[data-id="'+val+'"]').children()[1]).text());
        var mult = 1
        if ($(this).closest('form').find('#'+modelName+'MultiSet-multiplier').length){
            mult = parseInt($(this).closest('form').find('#'+modelName+'MultiSet-multiplier').val());
        }
        amount += 1*mult;
        $($(added.find('tr[data-id="'+val+'"]').children()[1]).children()[0]).text(amount);
    } else {
        var row = '<tr data-id="'+val+'"><td>'+text+'</td><td><button type="buttton" class="btn btn-sm btn-danger '+modelName+'MultiSet-remove">1</button></td>'
        if ($(this).closest('form').find('#'+modelName+'MultiSet-multiplier').length){
            row += '<td><button type="buttton" class="btn btn-sm btn-danger '+modelName+'MultiSet-delete"><i class="fa fa-trash"></i></button></td>'
        }
        row += '</tr>'
        added.append(row)
    }
    refreshInput($(this).closest('form'))
    return false;
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
