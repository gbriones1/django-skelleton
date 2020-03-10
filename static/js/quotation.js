var customers = [];
var quotations = [];
var pricelists = [];
var orgSto = [];
var stoPro = [];
var pergentages = [];
var pricelistrelated = {};
var storages = {};

$.when(getObjectFiltered("quotation", function(data) {quotations = data}), getObject("percentage"), getObject("storage_product"), getObject("organization_storage"), getObject("customer"), getObject("pricelist")).done(function (){
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    pricelists = JSON.parse(sessionStorage.getItem("pricelist") || "[]")
    percentages = JSON.parse(sessionStorage.getItem("percentage") || "[]")
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
        var total = 0
        item.quotation_product_set.forEach(function (item2){
            total += item2.price * item2.amount
        })
        item.quotation_others_set.forEach(function (item2){
            total += item2.price * item2.amount
        })
        total += parseFloat(item.service)
        total -= parseFloat(item.discount)
        item.total = total.toFixed(2)
        item.authorized_name = "No"
        if (item.authorized){
            item.authorized_name = "Si"
        }
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
            field: 'authorized_name',
            title: 'Autorizado',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'total',
            title: 'Total',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'action',
            title: 'Acciones',
            formatter: actionFormatter,
            width: actions.length*60,
            align: 'center',
            events: {
                'click .edit': quotationEditEvent,
                'click .delete': deleteEvent,
                'click .output': outputEvent,
                'click .view': viewEvent,
                'click .mail': mailEvent,
                'click .sell': sellEvent
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
    $(this).closest('.multiSet-container').find('.multiSet-table tbody tr').each( function () {
        $(this).attr("data-base_price", $(this).attr("data-price"));
    });
});

$(document).on('change', 'select[name="base_price"]', function(){
    var percentageName = $(this).val()
    var form = $(this).closest('form')
    var data = getFormData(form)
    if (percentageName == 'pricelist'){
        form.find('select#id_customer').val("");
        form.find('select#id_customer').attr('disabled', 'disabled');
        form.find('select#id_pricelist').removeAttr('disabled');
        if (data.pricelist){
            form.find('.multiSet-table tbody tr').each(function () {
                $(this).show()
                $(this).attr("data-price", pricelistrelated[data.pricelist][$(this).data("id")]);
            });
            renderFilter(form, data.pricelist);
        }
        else {
            form.find('.multiSet-table tbody tr').each(function () {
                $(this).hide();
            });
        }
    }
    else {
        form.find('select#id_customer').removeAttr('disabled');
        form.find('select#id_pricelist').val('');
        form.find('select#id_pricelist').attr('disabled', 'disabled');
        form.find('.multiSet-table tbody tr').each(function () {
            $(this).show()
            var basePrice = parseFloat($(this).attr("data-base_price"));
            var percentage = 0
            if (percentageName){
                for (index in percentages){
                    var max_price_limit = parseFloat(percentages[index].max_price_limit)
                    if (basePrice <= max_price_limit){
                        percentage = parseFloat(percentages[index][percentageName])
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
        form.find('.multiSet-table tbody tr').each(function () {
            $(this).show();
            $(this).attr("data-price", pricelistrelated[pricelistId][$(this).data("id")]);
        });
        form.find('select#id_base_price').attr('disabled', 'disabled');
        var search = form.find('.multiSet-search-available').val()
        var table = form.find('.multiSet-table')
        applySearch(search, table)
        renderFilter(form, parseInt(form.find('select#id_pricelist').val()))
    }
    else{
        form.find('select#id_base_price').removeAttr('disabled');
        form.find('.multiSet-table tbody tr').each(function () {
            $(this).hide();
        });
    }
});

function renderFilter(form, pricelistId) {
    var related = pricelistrelated[pricelistId];
    form.find('.multiSet-table tbody tr').each(function () {
        if (!related || !related[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('click', '.multiSet-add', function(){
    if($(this).closest('form').find('select#id_pricelist').val()){
        $(this).closest('form').find('select#id_base_price').attr('disabled', 'disabled');
    }
    else {
        $(this).closest('form').find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
    }
    return false;
});

$(document).on('click', '.multiSet-add-all', function(){
    if($(this).closest('form').find('select#id_pricelist').val()){
        $(this).closest('form').find('select#id_base_price').attr('disabled', 'disabled');
    }
    else {
        $(this).closest('form').find('select#id_base_price option[value="pricelist"]').attr('disabled', 'disabled');
    }
    return false;
});

$(document).on('click', '.multiSet-delete', function(){
    $('input.multiset').each(function functionName() {
        if ($(this).closest('form').find('.multiSet-added tbody').children().length == 0){
            if (!$(this).closest('form').find('select#id_pricelist').val()){
                $(this).closest('form').find('select#id_base_price').removeAttr('disabled');
                $(this).closest('form').find('select#id_base_price option[value="pricelist"]').removeAttr('disabled');
            }
        }
    })
    return false;
});

$(document).on('click', '.multiSet-delete-all', function(){
    $('input.multiset').each(function functionName() {
        if (!$(this).closest('form').find('select#id_pricelist').val()){
            $(this).closest('form').find('select#id_base_price').removeAttr('disabled');
            $(this).closest('form').find('select#id_base_price option[value="pricelist"]').removeAttr('disabled');
        }
    })
    return false;
});

function quotationEditEvent(e, value, data, index) {
    editEvent(e, value, data, index)
    var form = $("#edit form");
    if (data.pricelist){
        form.find('.multiSet-table tbody tr').each(function () {
            $(this).show()
            $(this).attr("data-price", pricelistrelated[data.pricelist][$(this).data("id")]);
        });
        renderFilter(form, data.pricelist)
        form.find('select[name="base_price"]').val("pricelist")
    }
    initialMultiSetData(form.find('input[name="quotation_product_set"]'), data.quotation_product_set)
    initialMultiSetData(form.find('input[name="quotation_others_set"]'), data.quotation_others_set)
}

$('.multiSet-container').each(function () {
    $(this).find('table.multiSet-table tr').each(function(){
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
    form.find('table.multiSet-table tr').each(function(){
        if (!inStorage || !inStorage[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('change', '#output.modal form select#id_organization_storage', function() {
    var form = $(this).closest('form')
    form.find('table.multiSet-table tr').each(function(){
        $(this).show()
    });
    var search = form.find('.multiSet-search-available').val()
    var table = form.find('.multiSet-table')
    applySearch(search, table)
    renderFilterForOutput(form)
});

function outputEvent (e, value, data, index) {
    var form = $("#output form");
    form .submit(function() {
        return false;
    });
    form[0].reset();
    form.find('input[name="destination"]').val(data.customer);
    initialMultiSetData(form.find('input#id_movement_product_set'), data.quotation_product_set);
    refreshMutliSetInputs(form);
    renderFilterForOutput(form);
}

$(document).on('click', 'button.do-output', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form');
    refreshMutliSetInputs(form);
    var formData = new FormData(form.get(0));
    $.ajax({
        url: "/database/api/output/",
        data: new URLSearchParams(formData).toString(),
        type: 'POST',
        success: function (data) {
            sessionStorage.removeItem('storage_product')
            window.location = '/database/output/';
        },
        error: function (data) {
            button.attr('disabled', false)
            handleErrorAlerts(data)
        }
    });
});

function viewEvent (e, value, data, index) {
    window.location = '/database/quotation/'+data.id;
};

function mailEvent (e, value, data, index) {
    var mailform = $("#mail form");
    mailform .submit(function() {
        return false;
    });
    mailform[0].reset();
    mailform.find('input[name="id"]').val(data['id']);
}

$(document).on('click', 'button.do-mail', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form');
    refreshMutliSetInputs(form);
    var formData = new FormData(form.get(0));
    var id = JSON.parse(formData.get('id'))
    $.ajax({
        url: "/database/api/quotation/"+id+"/",
        data: formData,
        contentType: false,
        processData: false,
        type: 'PUT',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            button.attr('disabled', false)
            handleErrorAlerts(data)
        }
    });
});

function sellEvent (e, value, data, index) {
    var form = $("#sell form");
    form[0].reset();
    form.find('input[name="customer"]').val(data.customer);
    form.find('input[name="price"]').val(data.total);
}

$(document).on('click', 'button.do-sell', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form');
    refreshMutliSetInputs(form);
    var formData = new FormData(form.get(0));
    $.ajax({
        url: "/database/api/sell/",
        data: new URLSearchParams(formData).toString(),
        type: 'POST',
        success: function (data) {
            window.location = '/database/sell/';
        },
        error: function (data) {
            button.attr('disabled', false)
            handleErrorAlerts(data)
        }
    });
});