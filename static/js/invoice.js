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
            title: 'Numero',
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
    var table = '<table><tr><th>Fecha</th><th>Pago</th><th>Forma de Pago</th></tr><tbody>'
    row.payment_set.forEach(function(item) {
        var method = ''
        switch(item.method) {
            case "C":
                method = "Efectivo"
                break;
            case "T":
                method = "Transferencia"
                break;
            case "K":
                method = "Cheque"
                break;
        }
        table += '<tr><td>'+item.date+'</td><td>$'+item.amount+'</td><td>'+method+'</td></tr>'
    })
    table += '</tbody></table>'
    return table
}