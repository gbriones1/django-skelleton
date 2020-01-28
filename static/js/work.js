var works = [];

$.when(getObjectFiltered("work", function(data) {works = data})).done(function (){
    buildTable()
});

function buildTable (){
    data = works
    $('#table').bootstrapTable({
        columns: [{
            checkbox: true
        }, {
            field: 'number',
            title: 'Folio',
            sortable: true,
            filterControl: 'input'
        }, {
            field: 'date',
            title: 'Fecha',
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