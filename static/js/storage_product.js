var stoPro = [];
var products = [];
var orgSto = [];

$.when(getObject("product"), getObject("storage_product"), getObject("organization_storage")).done(function (){
    stoPro = JSON.parse(sessionStorage.getItem("storage_product") || "[]")
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    buildTable()
});

function buildTable (){
    orgStoNames = {}
    orgSto.forEach(function (item, index) {
        orgStoNames[item.id] = item.organization_name + " - " + item.storage_type_name
    });
    productNames = {}
    products.forEach(function (item, index) {
        productNames[item.id] = item.code + " - " + item.name + " - " + item.description
    });
    data = []
    stoPro.forEach(function (item, index) {
        item.organization_storage_name = orgStoNames[item.organization_storage]
        item.product_name = productNames[item.product]
        data.push(item)
    })
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        }, {
            field: 'product_name',
            title: 'Refaccion',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'organization_storage_name',
            title: 'Almacen',
            sortable: true,
            filterControl: 'select'
        }, {
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
            field: 'action',
            title: 'Acciones',
            formatter: actionFormatter,
            width: actions.lenght*60,
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