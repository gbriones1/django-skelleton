var brands = [];

$.when(getObject("percentage")).done(function (){
    brands = JSON.parse(sessionStorage.getItem("percentage") || "[]")
    buildTable()
});

function buildTable (){
    data = brands
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        },{
            field: 'max_price_limit',
            title: 'Limite maximo de precio',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'sale_percentage_1',
            title: 'Porcentaje de venta 1',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'sale_percentage_2',
            title: 'Porcentaje de venta 2',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'sale_percentage_3',
            title: 'Porcentaje de venta 3',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'service_percentage_1',
            title: 'Porcentaje de servicio 1',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'service_percentage_2',
            title: 'Porcentaje de servicio 2',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'service_percentage_3',
            title: 'Porcentaje de servicio 3',
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