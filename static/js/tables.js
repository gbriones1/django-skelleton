function filter_data(data) {
    for (field in urlParams){
        if (data[field] != urlParams[field]){
            return false
        }
    }
    return true
}

function build_table(table, data, actions, selectable) {
    var body = $(table.find('tbody'));
    var headers = $(table.find('thead tr th'));
    for (index in data){
        if (filter_data(data[index])){
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
                        var value = data[index][$(headers[i]).attr('data-name')]
                        if (typeof(value) == "object" && value.length > 0){
                            // value = JSON.stringify(value);
                            var subt = $('<table>')
                            var subh = $('<thead>')
                            var subb = $('<tbody>')
                            var subhr = $('<tr>')
                            for (field_index in Object.keys(value[0])){
                                subhr.append($("<th>").text(Object.keys(value[0])[field_index]))
                            }
                            subh.append(subhr)
                            for (reg_index in value){
                                var subbr = $('<tr>')
                                for (subdata in value[reg_index]){
                                    subbr.append($("<td>").text(value[reg_index][subdata]))
                                }
                                subb.append(subbr)
                            }
                            subt.append(subh)
                            subt.append(subb)
                            tr.append($('<td>').append(subt))
                        }
                        else{
                            tr.append($('<td>').text(value));
                        }
                    }
                }
            }
            $.each(data[index], function( key, value ) {
                if (typeof(value) == "object"){
                    value = JSON.stringify(value);
                }
                tr.attr("data-"+key, value);
            });
            body.append(tr);
        }
    }
    $(table.find('tfoot th')).each( function () {
        var title = $(this).text();
        var width = $(this).width();
        if (title){
            $(this).html( '<input class="form-control" type="text" placeholder="Search '+title+'" style="width: 100%" />' );
            $(this).css('padding-left', '0px')
            $(this).css('padding-right', '0px')
        }
    } );
    // table.find('tfoot tr').appendTo('#'+table.attr("id")+' thead')
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
        "sScrollY": ($(window).height()-370)+"px",
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
    // table.closest('.dataTables_scroll').find('.dataTables_scrollFoot table').appendTo('.dataTables_scrollHeadInner')
    dt.columns().every( function () {
        var that = this;
        $('input', this.footer()).on('keyup change', function () {
            if (that.search() !== this.value) {
                that.search(this.value).draw();
            }
        });
    });
}


$('table.use-rest').each(function () {
    var table = $(this);
    var name = table.attr("id");
    $('.loading').show()
    if (name + "-update" in messages){
        var oldupdate = sessionStorage.getItem(name + "-update")
        if (oldupdate && (oldupdate < messages[name + "-update"])) {
            sessionStorage.removeItem(name)
        }
        sessionStorage.setItem(name + "-update", messages[name + "-update"]);
    }
    else{
        sessionStorage.setItem(name + "-update", new Date().getTime()+"");
    }
    if (!sessionStorage.getItem(name)){
        $.get( window.location.origin + table.data().rest, function( data ) {
            sessionStorage.setItem(name, JSON.stringify(data));
            build_table(table, data)
            $('.loading').hide()
        });
        console.log("fetched");
    }
    else{
        console.log("cached");
        build_table(table, JSON.parse(sessionStorage.getItem(name)))
        $('.loading').hide()
    }
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var data = $(this).closest('tr').data()
    var editform = $("#edit form");
    editform[0].reset();
    for (key in data){
        editform.find('input[name="'+ key +'"]').val(data[key]);
    }
});

$(document).on('click', 'button[data-target="#delete"]', function () {
    var data = $(this).closest('tr').data()
    var deleteform = $("#delete form");
    deleteform[0].reset();
    deleteform.find('input[name="id"]').val(data['id']);
});

$(document).on('click', 'button[data-target="#multi-delete"]', function () {
    var data = []
    $('input.checkthis').each(function() {
        if(this.checked){
            data.push($(this).closest('tr').data('id'));
        }
    });
    var deleteform = $("#multi-delete form");
    deleteform[0].reset();
    deleteform.find('input[name="ids"]').val(JSON.stringify(data));
});
