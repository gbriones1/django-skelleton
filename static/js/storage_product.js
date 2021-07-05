var stoPro = [];
var products = [];
var orgSto = [];
var proInSto = {}

var columns = [{
    checkbox: true
}, {
    field: 'product_name',
    title: 'Refaccion',
    sortable: true,
    filterControl: 'select'
}, {
    field: 'provider_name',
    title: 'Proveedor',
    sortable: true,
    filterControl: 'select'
}, {
    field: 'organization_storage_name',
    title: 'Almacen',
    sortable: true,
    filterControl: 'select'
}, {
    field: 'price',
    title: 'Precio',
    sortable: true,
    filterControl: 'input'
}, {
    field: 'value',
    title: 'Valor en existencia',
    sortable: true,
    filterControl: 'input'
},  {
    field: 'amount',
    title: 'En existencia',
    sortable: true,
    filterControl: 'input'
}, {
    field: 'must_have',
    title: 'Deberia haber',
    sortable: true,
    filterControl: 'input'
}, {
    field: 'debt',
    title: 'Deuda',
    sortable: true,
    filterControl: 'input'
}]

if (actions.length){
    columns.push({
        field: 'action',
        title: 'Acciones',
        formatter: actionFormatter,
        width: actions.lenght*60,
        align: 'center',
        events: {
            'click .edit': editEvent,
            'click .delete': deleteEvent
        }
    })
}

$.when(getObject("product"), getObject("storage_product"), getObject("organization_storage")).done(function (){
    stoPro = JSON.parse(sessionStorage.getItem("storage_product") || "[]")
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    buildTable()
});

function buildTable (){
    orgStoNames = {}
    orgSto.forEach(function (item, index) {
        orgStoNames[item.id] = item.organization_name + " - " + item.storage_type_name
        proInSto[item.id] = {}
    });
    productNames = {}
    providerIds = {}
    productPrices = {}
    products.forEach(function (item, index) {
        productNames[item.id] = item.code + " - " + item.name + " - " + item.description
        providerIds[item.id] = item.provider
        productPrices[item.id] = item.price
    });
    providerNames = {}
    providers.forEach(function (item, index) {
        providerNames[item.id] = item.name
    });
    data = []
    stoPro.forEach(function (item, index) {
        item.organization_storage_name = orgStoNames[item.organization_storage]
        item.product_name = productNames[item.product]
        item.provider_name = providerNames[providerIds[item.product]]
        item.price = productPrices[item.product]
        item.value = productPrices[item.product] * item.amount
        item.debt = productPrices[item.product] * (item.must_have - item.amount)
        if (item.debt < 0){
            item.debt = 0
        }
        data.push(item)
        proInSto[item.organization_storage][item.product] = true
    })
    $('#table').bootstrapTable({
        columns: columns,
        pagination: true,
        filterControl: true,
        height: 600,
        data: data
    })
}

$('select#id_product').attr('disabled', 'disabled');

$(document).on('change', 'select#id_organization_storage', function(){
    var selectedOrgSto = $(this).val()
    $('select#id_product > option').each(function (){
        // console.log($(this));
        var prodId = $(this).val()
        $(this).show();
        if (proInSto[selectedOrgSto][prodId] == true){
            $(this).hide();
        }
    })
    $('select#id_product').removeAttr('disabled');
})