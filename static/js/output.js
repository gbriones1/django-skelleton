var outputs = [];
var organizations = [];
var orgSto = [];
var products = [];
var employees = [];
var customers = [];
var productNames = {};
var productProviders = {};
var storages = {};

$.when(getObjectFiltered("output", function(data) {outputs = data}), getObject("product"), getObject("organization"), getObject("organization_storage"), getObject("employee"), getObject("customer"), getObject("storage_product")).done(function (){
    organizations = JSON.parse(sessionStorage.getItem("organization") || "[]")
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    employees = JSON.parse(sessionStorage.getItem("employee") || "[]")
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    stoPro = JSON.parse(sessionStorage.getItem("storage_product") || "[]")
    $('#new.modal form').each(function () {
        renderFilter($(this));
    });
    buildTable()
});

function buildTable (){
    employeeNames = {}
    employees.forEach(function (item, index) {
        employeeNames[item.id] = item.name
    });
    customerNames = {}
    customers.forEach(function (item, index) {
        customerNames[item.id] = item.name
    });
    organizationNames = {}
    organizations.forEach(function (item, index) {
        organizationNames[item.id] = item.name
    });
    orgStoNames = {}
    orgSto.forEach(function (item, index) {
        storages[item.id] = {};
        orgStoNames[item.id] = item.organization_name + " - " + item.storage_type_name
    });
    stoPro.forEach(function (item) {
        storages[item.organization_storage][item.product] = item.amount
    });
    products.forEach(function (item, index) {
        productNames[item.id] = item.code + " - " + item.name + " - " + item.description
        item.price_raw = item.price
        productProviders[item.id] = item.provider
    });
    data = []
    outputs.forEach(function (item){
        item['employee_name'] = employeeNames[item.employee]
        item['destination_name'] = customerNames[item.destination]
        item['replacer_name'] = organizationNames[item.replacer]
        item['storage_name'] = orgStoNames[item.organization_storage]
        var itemProducts = []
        item.movement_product_set.forEach(function (movement){
            itemProducts.push(productNames[movement.product])
        });
        item['products'] = itemProducts.join(",")
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
            field: 'employee_name',
            title: 'Trabajador',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'destination_name',
            title: 'Cliente',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'replacer_name',
            title: 'Repone',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'storage_name',
            title: 'Almacen',
            sortable: true,
            filterControl: 'select'
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
    var table = '<table><tr><th>Refaccion</th><th>Precio Unitario</th><th>Cantidad</th><th>Total</th></tr><tbody>'
    row.movement_product_set.forEach(function(item) {
        table += '<tr><td>'+productNames[item.product]+'</td><td>$'+item.price+'</td><td>'+item.amount+'</td><td>$'+(item.price*item.amount).toFixed(2)+'</td></tr>'
    })
    table += '</tbody></table>'
    return table
}

function productFormatter(element, row, index){
    return '<a class="detail-icon" href="#"><i class="fa fa-plus"></i></a><div style="display: none;">'+element+"</div>"
}

function renderFilter(form) {
    var selectedStorage = form.find('select#id_organization_storage').val();
    form.find('table#multiSet-table tr').each(function(){
        var inStorage = storages[selectedStorage];
        if (!inStorage){
            $(this).hide();
        }
        else if (!inStorage[$(this).data("id")]){
            $(this).hide();
        }
    });
}

$(document).on('change', '#new select#id_organization_storage', function() {
    var form = $(this).closest('form')
    form.find('table#multiSet-table tr').each(function(){
        $(this).show()
    });
    var search = form.find('#multiSet-search-available').val()
    var table = form.find('#multiSet-table')
    applySearch(search, table)
    renderFilter(form)
});

$(document).on('keyup change', '#multiSet-search-available', function() {
    renderFilter($(this).closest('form'))
});

$(document).on('click', 'button[data-target="#order"]', function () {
    var data = [];
    var movement_product_set = {}
    var orderform = $("#order form");
    $("#table").bootstrapTable('getSelections').forEach(function (item, index) {
        var curr_set = item.movement_product_set
        for (idx in curr_set){
            if (movement_product_set[curr_set[idx].product]){
                movement_product_set[curr_set[idx].product] += curr_set[idx].amount
            }
            else{
                movement_product_set[curr_set[idx].product] = curr_set[idx].amount
            }
        }
    });
    for (product in movement_product_set){
        data.push({'product':product, 'amount':movement_product_set[product]})
    }
    initialMultiSetData(orderform.find('input#id_order_product_set'), data);
    refreshMutliSetInputs(orderform);
});

$(document).on('click', 'button.do-order', function () {
    var orders = {};
    var form = $(this).closest('.modal-content').find('form');
    refreshMutliSetInputs(form);
    var formData = new FormData(form.get(0));
    var products = JSON.parse(formData.get('order_product_set'))
    for (idx in products) {
        if (orders[productProviders[products[idx].product]]){
            orders[productProviders[products[idx].product]]["order_product_set[0]"].push(products[idx])
        }
        else {
            orders[productProviders[products[idx].product]] = {
                provider: productProviders[products[idx].product],
                message: formData.get('message'),
                organization_storage: formData.get('organization_storage'),
                claimant: formData.get('claimant'),
                replacer: formData.get('replacer'),
                order_product_set: [products[idx]]
            }
        }
    }
    var calls = []
    for (key in orders){
        for (idx in orders[key].order_product_set){
            orders[key]['order_product_set['+idx+']'] = JSON.stringify(orders[key].order_product_set[idx])
        }
        orders[key].order_product_set = JSON.stringify(orders[key].order_product_set);
        calls.push(createOrder(orders[key]))
    }
    if (calls.length > 0){
        $.when.apply(null, calls).then(function () {
            window.location = '/database/order/'
        });
    }
});

function createOrder(data){
    return $.ajax({
        url: "/database/api/order/",
        data: new URLSearchParams(data).toString(),
        type: 'POST',
        success: function (data) {
            console.log('sucess');
        },
        error: function (data) {
            handleErrorAlerts(data)
        }
    });
}

$('.multiSet-container').each(function () {
    $(this).find('table#multiSet-table tr').each(function(){
        var priceRaw = $(this).data("price")
        var discount = $(this).data("discount")
        var price = (priceRaw - priceRaw*(discount/100)).toFixed(2)
        $(this).data("price-raw", priceRaw)
        $(this).data("price", price)
        $(this).attr("data-price", price)
    });
})