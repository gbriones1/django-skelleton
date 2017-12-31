var storages = []
$("#output form").find('select#id_organization_storage').attr('disabled', 'disabled');
$.getJSON("/database/special-api/instorage", function (json) {
    storages = json;
    $("#output form").find('select#id_organization_storage').removeAttr('disabled');
});

var pricelistrelated = []
$.getJSON("/database/special-api/pricelistrelated", function (json) {
    pricelistrelated = json;
});

$('input.multiset').each(function () {
    $(this).closest('.multiSet-container').find('#multiSet-table tbody tr').each( function () {
        $(this).attr("data-base_price", $(this).attr("data-price"));
    });
});

$('select#id_pricelist').attr('disabled', 'disabled');

$(document).on('click', 'button[data-target="#mail"]', function () {
    var data = $(this).closest('tr').data()
    var form = $("#mail form");
    form.find('input[name="id"]').val(data.id);
});

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
    for (opIndx in data.quotation_product_set){
        delete data.quotation_product_set[opIndx].id
    }
    initialMultiSetData(form.find('input#id_movement_product_set'), data.quotation_product_set);
    refreshMutliSetInputs(form);
    if (data.customer){
        form.find('select[name="destination"]').val(data.customer);
        form.find('select[name="destination"]').attr('disabled', 'disabled');
    }
    renderFilterForOutput(form);
});

function renderFilterForOutput(form) {
    var selectedStorage = form.find('select#id_organization_storage').val();
    var inStorage = storages[selectedStorage];
    form.find('table#multiSet-table tr').each(function(){
        if (!inStorage || !inStorage[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('keyup change', '#output.modal form #multiSet-search', function() {
    renderFilterForOutput($(this).closest('form'))
});

$(document).on('change', '#output.modal form select#id_organization_storage', function() {
    var form = $(this).closest('form')
    form.find('table#multiSet-table tr').each(function(){
        $(this).show()
    });
    var search = form.find('#multiSet-search-available').val()
    var table = form.find('#multiSet-table')
    applySearch(search, table)
    renderFilterForOutput(form)
});

$(document).on('click', '#output.modal form .multiSet-add', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '#output.modal form .multiSet-add-all', function(){
    $(this).closest('form').find('select#id_organization_storage').attr('disabled', 'disabled');
    return false;
});

$(document).on('click', '#output.modal form .multiSet-delete', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('#multiSet-added tbody').children().length == 0){
            $(this).closest('form').find('select#id_organization_storage').removeAttr('disabled');
        }
    })
    return false;
});

$(document).on('click', '#output.modal form .multiSet-delete-all', function(){
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
    var form = $(this).closest('form')
    if (percentageName == 'pricelist'){
        form.find('select#id_customer').val("");
        form.find('select#id_customer').attr('disabled', 'disabled');
        form.find('select#id_pricelist').removeAttr('disabled');
        form.find('#multiSet-table tbody tr').each(function () {
            $(this).hide();
        });
    }
    else {
        form.find('select#id_customer').removeAttr('disabled');
        form.find('select#id_pricelist').val('');
        form.find('select#id_pricelist').attr('disabled', 'disabled');
        var percentagesDef = JSON.parse(form.find('input#id_percentages').val())
        form.find('#multiSet-table tbody tr').each(function () {
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
        var pricelistId = form.find('select#id_pricelist').val();
        form.find('#multiSet-table tbody tr').each(function () {
            $(this).show();
            $(this).attr("data-price", pricelistrelated[pricelistId][$(this).data("id")]);
        });
        form.find('select#id_base_price').attr('disabled', 'disabled');
        var search = form.find('#multiSet-search-available').val()
        var table = form.find('#multiSet-table')
        applySearch(search, table)
        renderFilter(form)
    }
    else{
        form.find('select#id_base_price').removeAttr('disabled');
        form.find('#multiSet-table tbody tr').each(function () {
            $(this).hide();
        });
    }
});

function renderFilter(form) {
    var pricelistId = parseInt(form.find('select#id_pricelist').val());
    var related = pricelistrelated[pricelistId];
    form.find('#multiSet-table tbody tr').each(function () {
        if (!related || !related[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('click', '.multiSet-add', function(){
    if($(this).closest('form').find('select#id_pricelist').val()){
        $(this).closest('form').find('select#id_pricelist').attr('disabled', 'disabled');
        $(this).closest('form').find('select#id_base_price').attr('disabled', 'disabled');
    }
    else {
        $(this).closest('form').find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
    }
    return false;
});

$(document).on('click', '.multiSet-add-all', function(){
    if($(this).closest('form').find('select#id_pricelist').val()){
        $(this).closest('form').find('select#id_pricelist').attr('disabled', 'disabled');
        $(this).closest('form').find('select#id_base_price').attr('disabled', 'disabled');
    }
    else {
        $(this).closest('form').find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
    }
    return false;
});

$(document).on('click', '.multiSet-delete', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('#multiSet-added tbody').children().length == 0){
            if ($(this).closest('form').find('select#id_pricelist').val()){
                $(this).closest('form').find('select#id_pricelist').removeAttr('disabled');
            }
            else{
                $(this).closest('form').find('select#id_base_price').removeAttr('disabled');
                $(this).closest('form').find('select#id_base_price option[value="pricelist"]').removeAttr('disabled');
            }
        }
    })
    return false;
});

$(document).on('click', '.multiSet-delete-all', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('select#id_pricelist').val()){
            $(this).closest('form').find('select#id_pricelist').removeAttr('disabled');
        }
        else{
            $(this).closest('form').find('select#id_base_price').removeAttr('disabled');
            $(this).closest('form').find('select#id_base_price option[value="pricelist"]').removeAttr('disabled');
        }
    })
    return false;
});

$(document).on('submit', 'form', function(){
    $(this).find('select#id_pricelist').removeAttr('disabled');
    $(this).find('select#id_customer').removeAttr('disabled');
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var form = $("#edit form");
    form.find('#multiSet-table tbody tr').each(function () {
        $(this).show();
    });
    if (form.find('select#id_pricelist').val()){
        if (form.find('#multiSet-added tbody').children().length != 0){
            form.find('select#id_pricelist').attr('disabled', 'disabled');
        }
        form.find('select#id_base_price').val("pricelist");
        form.find('select#id_base_price').attr('disabled', 'disabled');
        form.find('select#id_customer').val('');
        form.find('select#id_customer').attr('disabled', 'disabled');
        renderFilter(form)
    }
    else {
        form.find('select#id_pricelist').attr('disabled', 'disabled');
        if (form.find('#multiSet-added tbody').children().length != 0){
            form.find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
        }
    }
    var value = form.find('input#id_quotation_product_set').val() || "[]"
    if (value){
        value = JSON.parse(value)
    }
    initialMultiSetData(form.find('input#id_quotation_product_set'), value)
});
