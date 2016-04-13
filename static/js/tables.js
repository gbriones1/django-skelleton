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
                tr.append($('<td>').text(data[index][$(headers[i]).attr('data-name')]));
            }
        }
        body.append(tr);
    }
}

function build_data_table(table) {
    table.dataTable({
        "sScrollY": ($(window).height()-320)+"px",
        "sScrollX": "98%",
        "bScrollCollapse": true,
        "bPaginate": false,
        "sDom": '<"top">rt<"bottom"lp><"clear">',
        "aoColumnDefs" : [{
            'bSortable' : false,
            // 'aTargets' : [ 0, -1, -2 ]
            }],
        "aaSorting": [[1,'asc']]
    });
}


$('table.use-rest').each(function () {
    console.log($(this).data());
    var table = $(this);
    $.get( window.location.origin + table.data().rest, function( data ) {
        build_table(table, data)
    });
});
