var orders = [];
var organizations = [];
var orgSto = [];
var products = [];
var employees = [];
var providers = [];
var productNames = {};
var productReferences = {};

$.when(getObjectFiltered("order", function(data) {orders = data}), getObject("product"), getObject("organization"), getObject("organization_storage"), getObject("employee"), getObject("provider")).done(function (){
    organizations = JSON.parse(sessionStorage.getItem("organization") || "[]")
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    employees = JSON.parse(sessionStorage.getItem("employee") || "[]")
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    $('#new.modal form').each(function () {
        renderFilter($(this));
    });
    $('#input.modal form').each(function () {
        renderFilter($(this));
    });
    buildTable()
});

function buildTable (){
    employeeNames = {}
    employees.forEach(function (item, index) {
        employeeNames[item.id] = item.name
    });
    providerNames = {}
    providers.forEach(function (item, index) {
        providerNames[item.id] = item.name
    });
    organizationNames = {}
    organizations.forEach(function (item, index) {
        organizationNames[item.id] = item.name
    });
    orgStoNames = {}
    orgSto.forEach(function (item, index) {
        orgStoNames[item.id] = item.organization_name + " - " + item.storage_type_name
    });
    products.forEach(function (item, index) {
        productNames[item.id] = item.code + " - " + item.name + " - " + item.description
        productReferences[item.id] = item
    });
    data = []
    orders.forEach(function (item){
        item['claimant_name'] = employeeNames[item.claimant]
        item['provider_name'] = providerNames[item.provider]
        item['replacer_name'] = organizationNames[item.replacer]
        item['storage_name'] = orgStoNames[item.organization_storage]
        
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
            field: 'claimant_name',
            title: 'Trabajador',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'provider_name',
            title: 'Provedor',
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
            field: 'status_display',
            title: 'Estado',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'action',
            title: 'Acciones',
            formatter: actionFormatter,
            width: actions.length*60,
            align: 'center',
            events: {
                'click .edit': editEvent,
                'click .delete': deleteEvent,
                'click .input': inputEvent,
                'click .mail': mailEvent
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
    var table = '<table><tr><th>Refaccion</th><th>Cantidad</th></tr><tbody>'
    row.order_product_set.forEach(function(item) {
        table += '<tr><td>'+productNames[item.product]+'</td><td>'+item.amount+'</td></tr>'
    })
    table += '</tbody></table>'
    return table
}

function renderFilter(form, value) {
    form.find('table#multiSet-table tr').each(function(){
        if (!(value == $(this).data("provider"))){
            $(this).hide();
        }
    });
}

$(document).on('change', 'select#id_provider', function() {
    var form = $(this).closest('form')
    form.find('table#multiSet-table tr').each(function(){
        $(this).show()
    });
    var search = form.find('#multiSet-search-available').val()
    var table = form.find('#multiSet-table')
    var selectedProvider = form.find('select#id_provider').val();
    applySearch(search, table)
    renderFilter(form, selectedProvider)
});

$(document).on('keyup change', '#multiSet-search-available', function() {
    var form = $(this).closest('form')
    var selectedProvider = form.find('[name="provider"]').val();
    renderFilter(form, selectedProvider)
});

function inputEvent (e, value, data, index) {
    var form = $("#input form");
    form .submit(function() {
        return false;
    });
    form[0].reset();
    form.find('input[name="id"]').val(data['id']);
    form.find('select[name="organization_storage"]').val(data['organization_storage']);
    form.find('input[name="provider"]').val(data['provider']);
    var search = form.find('#multiSet-search-available').val()
    var table = form.find('#multiSet-table')
    applySearch(search, table)
    renderFilter(form, data['provider'])
    for (idx in data.order_product_set){
        data.order_product_set[idx].price = productReferences[data.order_product_set[idx].product].price
        data.order_product_set[idx].discount = productReferences[data.order_product_set[idx].product].discount
    }
    initialMultiSetData(form.find('input.multiset'), data.order_product_set)
}

$(document).on('click', 'button.do-input', function () {
    var form = $(this).closest('.modal-content').find('form');
    refreshMutliSetInputs(form);
    var formData = new FormData(form.get(0));
    $.ajax({
        url: "/database/api/input/",
        data: new URLSearchParams(formData).toString(),
        type: 'POST',
        success: function (data) {
            window.location = '/database/input/'
        },
        error: function (data) {
            alert(data.responseText)
        }
    });
});

function mailEvent (e, value, data, index) {
    var mailform = $("#mail form");
    mailform .submit(function() {
        return false;
    });
    mailform[0].reset();
    mailform.find('input[name="id"]').val(data['id']);
    mailform.find('input[name="organization_storage"]').val(data['organization_storage']);
}

$(document).on('click', 'button.do-mail', function () {
    var form = $(this).closest('.modal-content').find('form');
    refreshMutliSetInputs(form);
    var formData = new FormData(form.get(0));
    var id = JSON.parse(formData.get('id'))
    $.ajax({
        url: "/database/api/order/"+id+"/",
        data: formData,
        contentType: false,
        processData: false,
        type: 'PUT',
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            alert(data.responseText)
        }
    });
});