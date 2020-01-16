var brands = [];

$.when(getObject("brand")).done(function (){
    brands = JSON.parse(sessionStorage.getItem("brand") || "[]")
    buildTable()
});

function buildTable (){
    data = brands
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
        data: data
    })
}