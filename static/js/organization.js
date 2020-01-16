var organizations = [];

$.when(getObject("organization")).done(function (){
    organizations = JSON.parse(sessionStorage.getItem("organization") || "[]")
    buildTable()
});
function buildTable (){
    data = organizations
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