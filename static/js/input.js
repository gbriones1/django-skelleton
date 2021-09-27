var inputs = [];
var orgSto = [];
var products = [];
var providers = [];
var organizations = [];
var productNames = {};
var productProviders = {};
var providerProducts = {};
var organizationsNames = {};

$.when(getObjectFiltered("input", function(data) {inputs = data}), getObject("provider"), getObject("product"), getObject("organization_storage"), getObject("organization")).done(function (){
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage") || "[]")
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    organizations = JSON.parse(sessionStorage.getItem("organization") || "[]")
    $('#new.modal form').each(function () {
        renderFilter($(this));
    });
    buildTable()
});

function buildTable (){
    orgStoNames = {}
    orgSto.forEach(function (item, index) {
        orgStoNames[item.id] = item.organization_name + " - " + item.storage_type_name
    });
    providerNames = {}
    providers.forEach(function (item, index) {
        providerNames[item.id] = item.name
        providerProducts[item.id] = {}
    });
    products.forEach(function (item, index) {
        productNames[item.id] = item.code + " - " + item.name + " - " + item.description
        providerProducts[item.provider][item.id] = true
        productProviders[item.id] = item.provider
    });
    organizations.forEach(function (item, index) {
        organizationsNames[item.id] = item.name
    });
    data = []
    inputs.forEach(function (item){
        item['storage_name'] = orgStoNames[item.organization_storage]
        item['provider_name'] = providerNames[item.provider]
        item['organization_name'] = organizationsNames[item.organization]
        data.push(item);
    })
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        }, {
            field: 'date',
            title: 'Fecha',
            sortable: true,
        }, {
            field: 'provider_name',
            title: 'Proveedor',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'invoice_number',
            title: 'Factura',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'storage_name',
            title: 'Almacen',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'organization_name',
            title: 'Organizacion',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'total',
            title: 'Total',
            formatter: totalFormatter,
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'products',
            title: 'Productos',
            formatter: productFormatter,
            width: 60,
            filterControl: 'input'
        }, {
            field: 'action',
            title: 'Acciones',
            formatter: actionFormatter,
            width: actions.length*60,
            align: 'center',
            events: {
                'click .edit': editEvent,
                'click .delete': deleteEvent
              }
        }],
        pagination: true,
        filterControl: true,
        height: 600,
        data: data,
        detailView: true,
        detailFormatter: detailViewFormatter
    })
}

function detailViewFormatter(index, row, element){
    var table = '<table style="float: left;margin-right: 50px;"><tr><th>Refaccion</th><th>Precio Unitario</th><th>Cantidad</th><th>Total</th></tr><tbody>'
    row.movement_product_set.forEach(function(item) {
        table += '<tr><td>'+productNames[item.product]+'</td><td>$'+item.price+'</td><td>'+item.amount+'</td><td>$'+(item.price*item.amount).toFixed(2)+'</td></tr>'
    })
    table += '</tbody></table>'
    if (row.evidence){
        table += '<img src="'+row.evidence+'" height="250">'
    }
    return table
}

function productFormatter(element, row, index){
    return '<a class="detail-icon" href="#"><i class="fa fa-plus"></i></a><div style="display: none;">'+element+"</div>"
}

function totalFormatter(element, row, index){
    var total = 0;
    row.movement_product_set.forEach(function(item){
        total += item.price*item.amount
    })
    return "$"+total.toFixed(2)
}

function renderFilter(form) {
    var selectedProvider = form.find('select[name="provider"]').val();
    form.find('table.multiSet-table tr').each(function(){
        $(this).show()
        var inStorage = providerProducts[selectedProvider];
        if (!inStorage){
            $(this).hide();
        }
        else if (!inStorage[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('change', '#new select[name="provider"]', function() {
    var form = $(this).closest('form')
    var search = form.find('.multiSet-search-available').val()
    var table = form.find('.multiSet-table')
    applySearch(search, table)
    renderFilter(form)
});

$(document).on('keyup change', '.multiSet-search-available', function() {
    renderFilter($(this).closest('form'))
});

$(document).on('click', 'button[data-target="#remove_photo"]', function () {
    var ids = []
    var form = $("#remove_photo form");
    $("#table").bootstrapTable('getSelections').forEach(function (item, index) {
        ids.push(item.id)
    });
    form.find('input[name="ids"]').val(JSON.stringify(ids));
});

$(document).on('click', 'button.do-remove_photo', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form');
    var data = new FormData(form.get(0));
    $.ajax({
        url: "/database/api/input/",
        data: new URLSearchParams(data).toString(),
        type: 'POST',
        success: function (data) {
            if (typeof prefetch !== "undefined"){
                prefetch.forEach(function(item) {
                    sessionStorage.removeItem(item)
                });
            }
            location.reload();
        },
        error: function (data) {
            button.attr('disabled', false)
            handleErrorAlerts(data)
        }
    });
});