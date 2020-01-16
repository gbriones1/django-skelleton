var inputs = [];
var orgSto = [];
var products = [];
var productNames = {};

$.when(getObjectFiltered("input", function(data) {inputs = data}), getObject("product"), getObject("organization_storage")).done(function (){
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    buildTable()
});

function buildTable (){
    orgStoNames = {}
    orgSto.forEach(function (item, index) {
        orgStoNames[item.id] = item.organization_name + " - " + item.storage_type_name
    });
    products.forEach(function (item, index) {
        productNames[item.id] = item.code + " - " + item.name + " - " + item.description
    });
    data = []
    inputs.forEach(function (item){
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