var products = [];
var customers = [];
var contacts = []

$.when(getObject("product"), getObject("customer"), getObject("customer_contact")).done(function (){
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    contacts = JSON.parse(sessionStorage.getItem("customer_contact") || "[]")
    products = JSON.parse(sessionStorage.getItem("product") || "[]")
    buildTable()
});

function buildTable (){
    contactLists = {}
    contacts.forEach(function (item, index) {
        if (item.phone == null){
            item.phone = ''
        }
        if (item.email == null){
            item.email = ''
        }
        (contactLists[item.customer] = contactLists[item.customer] || []).push(item);
    });
    data = []
    customers.forEach(function(item, index) {
        item.customer_contact_set = contactLists[item.id]
        data.push(item)
    });
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        },{
            field: 'name',
            title: 'Nombre',
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
    var table = '<table><tr><th>Nombre</th><th>Departamento</th><th>Telefono</th><th>Email</th><th>Para cotizaciones</th><th>Para factura</th></tr>'
    row.customer_contact_set.forEach(function(item) {
        var quotationCheck = ''
        var invoiceCheck = ''
        if (item.for_quotation){
            quotationCheck = '<i class="fa fa-check-circle"></i>'
        }
        if (item.for_invoice){
            invoiceCheck = '<i class="fa fa-check-circle"></i>'
        }
        table += '<tr><td>'+item.name+'</td><td>'+item.department+'</td><td>'+item.phone+'</td><td>'+item.email+'</td><td>'+quotationCheck+'</td><td>'+invoiceCheck+'</td></tr>'
    })
    table += '</table>'
    return table
}