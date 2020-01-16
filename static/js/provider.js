var products = [];
var providers = [];
var contacts = []

$.when(getObject("product"), getObject("provider"), getObject("provider_contact")).done(function (){
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    contacts = JSON.parse(sessionStorage.getItem("provider_contact") || "[]")
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
        (contactLists[item.provider] = contactLists[item.provider] || []).push(item);
    });
    data = []
    providers.forEach(function(item, index) {
        item.provider_contact_set = contactLists[item.id]
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
    var table = '<table><tr><th>Nombre</th><th>Departamento</th><th>Telefono</th><th>Email</th><th>Para pedidos</th></tr>'
    row.provider_contact_set.forEach(function(item) {
        var ordersCheck = ''
        if (item.for_orders){
            ordersCheck = '<i class="fa fa-check-circle"></i>'
        }
        table += '<tr><td>'+item.name+'</td><td>'+item.department+'</td><td>'+item.phone+'</td><td>'+item.email+'</td><td>'+ordersCheck+'</td></tr>'
    })
    table += '</table>'
    return table
}