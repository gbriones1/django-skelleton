var products = [];
var brands = [];
var appliances = [];
var providers = [];

$.when(getObject("product"), getObject("brand"), getObject("provider"), getObject("appliance")).done(function (){
    brands = JSON.parse(sessionStorage.getItem("brand") || "[]")
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    appliances = JSON.parse(sessionStorage.getItem("appliance") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    buildTable()
});

function buildTable (){
    providerNames = {}
    brandNames = {}
    applianceNames = {}
    providers.forEach(function (item, index) {
        providerNames[item.id] = item.name
    });
    brands.forEach(function (item, index) {
        brandNames[item.id] = item.name
    });
    appliances.forEach(function (item, index) {
        applianceNames[item.id] = item.name
    });
    data = []
    products.forEach(function (item, index) {
        item.providerName = providerNames[item.provider]
        item.brandName = brandNames[item.brand]
        item.applianceName = applianceNames[item.appliance]
        item.realPrice = (item.price - item.price*(item.discount/100)).toFixed(2)
        data.push(item)
    })
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        },{
            field: 'code',
            title: 'Codigo',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'providerName',
            title: 'Proveedor',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'brandName',
            title: 'Marca',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'name',
            title: 'Producto',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'description',
            title: 'Descripcion',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'applianceName',
            title: 'Aplicacion',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'realPrice',
            title: 'Precio de Compra',
            sortable: true,
            filterControl: 'input',
            align: 'right'
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
        data: data
    })
}

$(document).on('click', 'button[data-target="#picture"]', function () {
    var data = $(this).closest('tr').data()
    var form = $("#picture form");
    form.find('input[name="id"]').val(data['id']);
});
