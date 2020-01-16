var orgSto = [];

$.when(getObject("organization_storage")).done(function (){
    orgSto = JSON.parse(sessionStorage.getItem("organization_storage"))
    buildTable();
});

function buildTable (){
    data = orgSto
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        }, {
            field: 'organization_name',
            title: 'Organizacion',
            sortable: true,
            filterControl: 'select'
        }, {
            field: 'storage_type_name',
            title: 'Almacen',
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