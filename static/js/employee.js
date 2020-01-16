var employees = [];

$.when(getObject("employee")).done(function (){
    employees = JSON.parse(sessionStorage.getItem("employee") || "[]")
    buildTable()
});

function buildTable (){
    data = employees
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        }, {
            field: 'name',
            title: 'Nombre',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'phone',
            title: 'Telefono',
            sortable: true,
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