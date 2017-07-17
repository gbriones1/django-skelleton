$('input.multiset').each(function () {
    $(this).closest('form').find('#ProductMultiSet-table tbody tr').each( function () {
        $(this).attr("data-base_price", $(this).attr("data-price"));
    });
    var editable = $(this).closest('form').find('#ProductMultiSet-table').attr('data-editable')
    $(this).closest('form').find('#ProductMultiSet-table').attr('data-editable-backup', editable)
});

$('select#id_pricelist').attr('disabled', 'disabled');

$(document).on('change', 'select#id_base_price', function(){
    var percentageName = $(this).val()
    if (percentageName == 'pricelist'){
        $('select#id_pricelist').removeAttr('disabled');
        $(this).closest('form').find('#ProductMultiSet-table').removeAttr('data-editable')
        $(this).closest('form').find('#ProductMultiSet-table tbody tr').each(function () {
            $(this).hide();
        });
    }
    else {
        $('select#id_pricelist').val('');
        $('select#id_pricelist').attr('disabled', 'disabled');
        var editableBackup = $(this).closest('form').find('#ProductMultiSet-table').attr('data-editable-backup')
        $(this).closest('form').find('#ProductMultiSet-table').attr('data-editable', editableBackup)
        var percentagesDef = JSON.parse($(this).closest('form').find('input#id_percentages').val())
        $(this).closest('form').find('#ProductMultiSet-table tbody tr').each(function () {
            $(this).show()
            var basePrice = parseFloat($(this).attr("data-base_price"));
            var percentage = 0
            if (percentageName){
                for (index in percentagesDef){
                    var max_price_limit = parseFloat(percentagesDef[index].max_price_limit)
                    if (basePrice <= max_price_limit){
                        percentage = parseFloat(percentagesDef[index][percentageName])
                        break;
                    }
                }
            }
            $(this).attr("data-price", (basePrice + (basePrice * percentage / 100)).toFixed(2));
        });
    }
});

$(document).on('change', 'select#id_pricelist', function(){
    var form = $(this).closest('form')
    if (form.find('select#id_pricelist').val()){
        form.find('#ProductMultiSet-table tbody tr').each(function () {
            $(this).show();
        });
        var search = form.find('#ProductMultiSet-search-available').val()
        var table = form.find('#ProductMultiSet-table')
        applySearch(search, table)
        renderFilter(form)
    }
});

function renderFilter(form) {
    var pricelistId = parseInt(form.find('select#id_pricelist').val());
    form.find('#ProductMultiSet-table tbody tr').each(function () {
        var related = $(this).data("pricelist_related")
        if (!(related.indexOf(pricelistId)+1)){
            $(this).hide();
        }
    });
}

$(document).on('click', '.ProductMultiSet-add', function(){
    if($(this).closest('form').find('select#id_pricelist').val()){
        $(this).closest('form').find('select#id_base_price').attr('disabled', 'disabled');
    }
    else {
        $(this).closest('form').find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
    }
    return false;
});

$(document).on('click', '.ProductMultiSet-add-all', function(){
    if($(this).closest('form').find('select#id_pricelist').val()){
        $(this).closest('form').find('select#id_base_price').attr('disabled', 'disabled');
    }
    else {
        $(this).closest('form').find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
    }
    return false;
});

$(document).on('click', '.ProductMultiSet-delete', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('#ProductMultiSet-added tbody').children().length == 0){
            if ($(this).closest('form').find('select#id_pricelist').val()){
                $(this).closest('form').find('select#id_pricelist').removeAttr('disabled');
            }
            $(this).closest('form').find('select#id_base_price').removeAttr('disabled');
            $(this).closest('form').find('select#id_base_price option[value="pricelist"]').removeAttr('disabled');
        }
    })
    return false;
});

$(document).on('click', '.ProductMultiSet-delete-all', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('select#id_pricelist').val()){
            $(this).closest('form').find('select#id_pricelist').removeAttr('disabled');
        }
        $(this).closest('form').find('select#id_base_price').removeAttr('disabled');
        $(this).closest('form').find('select#id_base_price option[value="pricelist"]').removeAttr('disabled');
    })
    return false;
});

$(document).on('submit', 'form', function(){
    $(this).find('select#id_pricelist').removeAttr('disabled');
});



$(document).on('click', 'button[data-target="#edit"]', function () {
    var form = $("#edit form");
    if (form.find('select#id_pricelist').val()){
        if (form.find('#ProductMultiSet-added tbody').children().length != 0){
            form.find('select#id_pricelist').attr('disabled', 'disabled');
        }
        form.find('select#id_base_price').val("pricelist");
        form.find('select#id_base_price').attr('disabled', 'disabled');
        form.find('#ProductMultiSet-table').removeAttr('data-editable')
    }
    else {
        var editableBackup = form.find('#ProductMultiSet-table').attr('data-editable-backup')
        form.find('#ProductMultiSet-table').attr('data-editable', editableBackup)
        form.find('select#id_pricelist').attr('disabled', 'disabled');
        if (form.find('#ProductMultiSet-added tbody').children().length != 0){
            form.find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
        }
    }
    var value = form.find('input#id_products').val() || "[]"
    if (value){
        value = JSON.parse(value)
    }
    initialMultiSetData(form, "Product", value)
});
