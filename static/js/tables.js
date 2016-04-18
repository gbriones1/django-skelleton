function build_table(table, data, actions, selectable) {
    var body = $(table.find('tbody'));
    var headers = $(table.find('thead tr th'));
    for (index in data){
        var tr = $('<tr>');
        if (table.data().selectable){
            tr.append($('<td><input type="checkbox" class="checkthis"></td>'));
        }
        for (i = 0; i < headers.length; i++) {
            if (!(table.data().selectable && i == 0)){
                if ($(headers[i]).hasClass('table-action')){
                    var action = $(headers[i]).data().json
                    tr.append($('<td align="center"><p data-pacement="top" data-toggle="tooltip" title="'+$(headers[i]).text()+'"><button class="btn btn-'+action.style+'" data-target="#'+action.name+'" data-toggle="modal"><i class="fa fa-'+action.icon+'"></i></button></p></td>'))
                }
                else{
                    tr.append($('<td>').text(data[index][$(headers[i]).attr('data-name')]));
                }
            }
        }
        body.append(tr);
    }
    build_data_table(table)
}

function build_data_table(table) {
    var unsortable = []
    var sorting = 0
    var headers = $(table.find('thead tr th'));
    if (table.data().selectable){
        unsortable.push(0)
        sorting = 1
    }
    for (i = 0; i < headers.length; i++){
        if ($(headers[i]).hasClass('table-action')){
            unsortable.push(i)
        }
    }
    var dt = table.DataTable({
        "sScrollY": ($(window).height()-320)+"px",
        "sScrollX": "100%",
        "bScrollCollapse": true,
        "lengthMenu": [[50, 100, -1], [50, 100, "All"]],
        "sDom": '<"top">rt<"bottom"lp><"clear">',
        "aoColumnDefs" : [{
            'bSortable' : false,
            'aTargets' : unsortable
            }],
        "aaSorting": [[sorting,'asc']]
    });
    console.log(dt)
}


$('table.use-rest').each(function () {
    var table = $(this);
    $('.loading').show()
    $.get( window.location.origin + table.data().rest, function( data ) {
        build_table(table, data)
        $('.loading').hide()
    });
});
