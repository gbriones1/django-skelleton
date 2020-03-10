var products = [];
var brands = [];
var appliances = [];
var providers = [];
var percentages = [];

$.when(getObject("product"), getObject("percentage"), getObject("brand"), getObject("provider"), getObject("appliance")).done(function (){
    brands = JSON.parse(sessionStorage.getItem("brand") || "[]")
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    appliances = JSON.parse(sessionStorage.getItem("appliance") || "[]")
    percentages = JSON.parse(sessionStorage.getItem("percentage") || "[]")
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
    percentages.sort((a, b) => parseFloat(a['max_price_limit']) - parseFloat(b['max_price_limit']))
    data = []
    products.forEach(function (item, index) {
        item.provider_name = providerNames[item.provider]
        item.brand_name = brandNames[item.brand]
        item.appliance_name = applianceNames[item.appliance]
        item.realPrice = (item.price - item.price*(item.discount/100)).toFixed(2)
        for (var percentage of percentages){
            if (parseFloat(percentage['max_price_limit']) >= parseFloat(item.realPrice)){
                item.percentage_1 = (parseFloat(item.realPrice)+(parseFloat(item.realPrice)*parseFloat(percentage['sale_percentage_1'])/100)).toFixed(2)
                item.percentage_2 = (parseFloat(item.realPrice)+(parseFloat(item.realPrice)*parseFloat(percentage['sale_percentage_2'])/100)).toFixed(2)
                item.percentage_3 = (parseFloat(item.realPrice)+(parseFloat(item.realPrice)*parseFloat(percentage['sale_percentage_3'])/100)).toFixed(2)
                break
            }
        }
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
            field: 'provider_name',
            title: 'Proveedor',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'brand_name',
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
            field: 'appliance_name',
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
            field: 'percentage_1',
            title: 'Precio de Venta 1',
            sortable: true,
            filterControl: 'input',
            align: 'right'
        }, {
            field: 'percentage_2',
            title: 'Precio de Venta 2',
            sortable: true,
            filterControl: 'input',
            align: 'right'
        }, {
            field: 'percentage_3',
            title: 'Precio de Venta 3',
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
