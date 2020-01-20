var customers = [];
var pricelists = [];

$.when(getObject("pricelist"), getObject("customer")).done(function (){
    pricelists = JSON.parse(sessionStorage.getItem("pricelist") || "[]")
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    buildTable()
});

function buildTable (){
    customerNames = {}
    customers.forEach(function (item, index) {
        customerNames[item.id] = item.name
    });
    data = []
    pricelists.forEach(function (item, index) {
        item.customer_name = customerNames[item.customer]
        data.push(item)
    })
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        },{
            field: 'customer_name',
            title: 'Cliente',
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
        data: data
    })
}

$('input.multiset').each(function () {
    $(this).closest('form').find('#multiSet-table tbody tr').each( function () {
        $(this).attr("data-base_price", $(this).attr("data-price"));
    })
});

$(document).on('change', 'select#id_base_price', function(){
    var percentageName = $(this).val()
    var percentagesDef = JSON.parse($(this).closest('form').find('input#id_percentages').val())
    $(this).closest('form').find('#multiSet-table tbody tr').each(function () {
        var basePrice = parseFloat($(this).attr("data-base_price"));
        var percentage = 0
        if (percentageName){
            for (index in percentagesDef){
                var max_price_limit = parseFloat(percentagesDef[index].max_price_limit)
                if (basePrice <= max_price_limit){
                    percentage = parseFloat(percentagesDef[index][percentageName])
                    break;
                }
            }
        }
        $(this).attr("data-price", (basePrice + (basePrice * percentage / 100)).toFixed(2));
    })
});
