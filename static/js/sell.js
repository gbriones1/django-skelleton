var sells = [];
var customers = [];

$.when(getObjectFiltered("sell", function(data) {sells = data}), getObject("customer")).done(function (){
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    buildTable()
});

function buildTable (){
    customerNames = {}
    customers.forEach(function (item, index) {
        customerNames[item.id] = item.name
    });
    data = []
    sells.forEach(function (item, index) {
        item.customer_name = customerNames[item.customer]
        item.paid_status = "No"
        if (item.paid){
            item.paid_status = "Si"
        }
        item.invoiced_status = "No"
        if (item.invoiced){
            item.invoiced_status = "Si"
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
            title: 'Folio',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'customer_name',
            title: 'Cliente',
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
            field: 'invoiced_status',
            title: 'Facturado',
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
    var table = '<table><tr><th>Fecha</th><th>Pago</th></tr><tbody>'
    row.collection_set.forEach(function(item) {
        table += '<tr><td>'+item.date+'</td><td>$'+item.amount+'</td></tr>'
    })
    table += '</tbody></table>'
    return table
}