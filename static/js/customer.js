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
            filterControl: 'input'
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
    if (row.customer_contact_set){
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
    }
    table += '</table>'
    return table
}

$(document).on('click', 'button[data-target="#merge"]', function(){
    var form = $('#merge').find('form')
    var ids = [];
    $("#table").bootstrapTable('getSelections').forEach(function (item, index) {
        ids.push(item.id)
    });
    form.find('select[name="name"]').val("")
    form.find('select[name="name"] option').each(function (){
        $(this).hide();
        if (ids.includes(parseInt($(this).val()))){
            $(this).show()
        }
    });
    form.find('input[name="ids"]').val(JSON.stringify(ids))
});

$(document).on('click', 'button.do-merge', function() {
    var button = $(this)
    var form = $(this).closest('.modal-content').find('form');
    var formData = new FormData(form.get(0));
    var id = JSON.parse(formData.get('name'))
    if (id) {
        button.attr('disabled', true)
        $.ajax({
            url: "/database/merge/customer/"+id+"/",
            data: formData,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function (data) {
                if (typeof prefetch !== "undefined"){
                    prefetch.forEach(function(item) {
                        sessionStorage.removeItem(item)
                    });
                }
                location.reload();
            },
            error: function (data) {
                button.attr('disabled', false)
                handleErrorAlerts(data)
            }
        });
    } else {
        createAlert("Se debe seleccionar un nombre verdadero", "warning")
    }
});