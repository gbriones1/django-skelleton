var customers = [];
var quotations = [];
var pricelists = [];
var orgSto = [];
var stoPro = [];
var pricelistrelated = {};
var storages = {};

$.when(getObjectFiltered("quotation", function(data) {quotations = data}), getObject("storage_product"), getObject("organization_storage"), getObject("customer"), getObject("pricelist")).done(function (){
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    pricelists = JSON.parse(sessionStorage.getItem("pricelist") || "[]")
    stoPro = JSON.parse(sessionStorage.getItem("storage_product") || "[]")
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage") || "[]")
    buildTable()
});

function buildTable (){
    customerNames = {}
    customers.forEach(function (item, index) {
        customerNames[item.id] = item.name
    });
    pricelists.forEach(function(item){
        productPrices = {}
        item.pricelist_product_set.forEach(function (item){
            productPrices[item.product] = item.price
        })
        pricelistrelated[item.id] = productPrices
    })
    orgSto.forEach(function (item, index) {
        storages[item.id] = {};
    });
    stoPro.forEach(function (item) {
        storages[item.organization_storage][item.product] = item.amount
    });
    data = []
    quotations.forEach(function (item, index) {
        item.customer_name = customerNames[item.customer]
        data.push(item)
    })
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        }, {
            field: 'id',
            title: 'Numero de Cotizacion',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'date',
            title: 'Fecha',
            sortable: true,
        }, {
            field: 'customer_name',
            title: 'Cliente',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'unit',
            title: 'Unidad',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'plates',
            title: 'Placas',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'work_number',
            title: 'Hoja de trabajo',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'action',
            title: 'Acciones',
            formatter: actionFormatter,
            width: actions.length*60,
            align: 'center',
            events: {
                'click .edit': editEvent,
                'click .delete': deleteEvent,
                'click .output': outputEvent,
                'click .view': viewEvent
              }
        }],
        pagination: true,
        filterControl: true,
        height: 600,
        data: data
    })
}

$('select#id_pricelist').attr('disabled', 'disabled');

$('input.multiset').each(function () {
    $(this).closest('.multiSet-container').find('#multiSet-table tbody tr').each( function () {
        $(this).attr("data-base_price", $(this).attr("data-price"));
    });
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

$('.multiSet-container').each(function () {
    $(this).find('table#multiSet-table tr').each(function(){
        var priceRaw = $(this).data("price")
        var discount = $(this).data("discount")
        var price = (priceRaw - priceRaw*(discount/100)).toFixed(2)
        $(this).data("price-raw", priceRaw)
        $(this).data("price", price)
        $(this).data("base_price", price)
        $(this).attr("data-price", price)
        $(this).attr("data-base_price", price)
    });
})

function renderFilterForOutput(form) {
    var selectedStorage = form.find('select#id_organization_storage').val();
    var inStorage = storages[selectedStorage];
    form.find('table#multiSet-table tr').each(function(){
        if (!inStorage || !inStorage[$(this).data("id")]){
            $(this).hide();
        }
    });
}

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

function outputEvent (e, value, data, index) {
    var form = $("#output form");
    form .submit(function() {
        return false;
    });
    form[0].reset();
    initialMultiSetData(form.find('input#id_movement_product_set'), data.quotation_product_set);
    refreshMutliSetInputs(form);
    renderFilterForOutput(form);
}

$(document).on('click', 'button.do-output', function () {
    var form = $(this).closest('.modal-content').find('form');
    refreshMutliSetInputs(form);
    var formData = new FormData(form.get(0));
    $.ajax({
        url: "/database/api/output/",
        data: new URLSearchParams(formData).toString(),
        type: 'POST',
        success: function (data) {
            window.location = '/database/output/';
        },
        error: function (data) {
            handleErrorAlerts(data)
        }
    });
});


function viewEvent (e, value, data, index) {
    window.location = '/database/quotation/'+data.id;
};