$('input.multiset').each(function () {
    $(this).closest('form').find('#ProductMultiSet-table tbody tr').each( function () {
        $(this).attr("data-base_price", $(this).attr("data-price"));
    });
    var editable = $(this).closest('form').find('#ProductMultiSet-table').attr('data-editable')
    $(this).closest('form').find('#ProductMultiSet-table').attr('data-editable-backup', editable)
});

$('select#id_pricelist').attr('disabled', 'disabled');

$(document).on('click', 'button[data-target="#output"]', function () {
    var data = $(this).closest('tr').data()
    var form = $("#output form");
    form[0].reset();
    form.trigger("reset");
    form.find('select').each(function (){
        $(this).val("");
    });
    form.find('select[name="destination"]').removeAttr('disabled');
    form.find('select[name="organization_storage"]').removeAttr('disabled');
    initialMultiSetData(form, "Product", data.products);
    refreshMutliSetInputs(form);
    if (data.customer){
        form.find('select[name="destination"]').val(data.customer);
        form.find('select[name="destination"]').attr('disabled', 'disabled');
    }
    renderFilterForOutput(form);
});

function renderFilterForOutput(form) {
    var selectedStorage = form.find('select#id_organization_storage').val();
    form.find('table#ProductMultiSet-table tr').each(function(){
        var inStorage = $(this).data("in_storage");
        if (!(selectedStorage in inStorage)){
            $(this).hide();
        } else if (inStorage[selectedStorage] == 0) {
            $(this).hide();
        }
    });
}

$(document).on('keyup change', '#output.modal form #ProductMultiSet-search', function() {
    renderFilterForOutput($(this).closest('form'))
});

$(document).on('change', '#output.modal form select#id_organization_storage', function() {
    var form = $(this).closest('form')
    form.find('table#ProductMultiSet-table tr').each(function(){
        $(this).show()
    });
    var search = form.find('#ProductMultiSet-search-available').val()
    var table = form.find('#ProductMultiSet-table')
    applySearch(search, table)
    renderFilterForOutput(form)
});

$(document).on('click', '#output.modal form .ProductMultiSet-add', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '#output.modal form .ProductMultiSet-add-all', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '#output.modal form .ProductMultiSet-delete', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('#ProductMultiSet-added tbody').children().length == 0){
            $(this).closest('form').find('select#id_organization_storage').removeAttr('disabled');
        }
    })
    return false;
});

$(document).on('click', '#output.modal form .ProductMultiSet-delete-all', function(){
    $('input.multiset').each(function functionName() {
        $(this).closest('form').find('select#id_organization_storage').removeAttr('disabled');
    })
    return false;
});

$('#output.modal form').submit(function () {
    $(this).find('select#id_organization_storage').removeAttr('disabled');
    $(this).find('select#id_destination').removeAttr('disabled');
});

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
