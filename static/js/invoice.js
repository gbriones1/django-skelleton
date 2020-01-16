var invoices = [];
var providers = [];

$.when(getObjectFiltered("invoice", function(data) {invoices = data}), getObject("provider")).done(function (){
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    buildTable()
});

function buildTable (){
    providerNames = {}
    providers.forEach(function (item, index) {
        providerNames[item.id] = item.name
    });
    data = []
    invoices.forEach(function (item, index) {
        item.provider_name = providerNames[item.provider]
        item.paid_status = "No"
        if (item.paid){
            item.paid_status = "Si"
        }
        data.push(item)
    })
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        }, {
            field: 'date',
            title: 'Fecha',
            sortable: true,
        }, {
            field: 'number',
            title: 'Factura',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'provider_name',
            title: 'Proveedor',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'price',
            title: 'Precio',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'due',
            title: 'Caduca',
            sortable: true,
        }, {
            field: 'paid_status',
            title: 'Pagado',
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
    var table = '<table><tr><th>Pago</th><th>Fecha</th></tr><tbody>'
    row.payment_set.forEach(function(item) {
        table += '<tr><td>'+0+'</td><td>$'+0+'</td></tr>'
    })
    table += '</tbody></table>'
    return table
}