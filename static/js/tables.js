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
        // if (filter_data(data[index])){
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
                        if (value && typeof(value) == "object" && value.length > 0){
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
                                    if (typeof(value[reg_index][subdata]) == "object"){
                                        var subt2 = $('<table>')
                                        // var subh2 = $('<thead>')
                                        var subb2 = $('<tbody>')
                                        // var subhr2 = $('<tr>')
                                        // for (field_index in Object.keys(value[reg_index][subdata])){
                                        //     subhr2.append($("<th>").text(Object.keys(value[reg_index][subdata])[field_index]))
                                        // }
                                        // subh2.append(subhr2)
                                        var subbr2 = $('<tr>')
                                        for (reg_index2 in value[reg_index][subdata]){
                                            subbr2.append($("<td>").text(value[reg_index][subdata][reg_index2]))
                                        }
                                        subb2.append(subbr2)
                                        // subt2.append(subh2)
                                        subt2.append(subb2)
                                        subbr.append($('<td>').append(subt2))
                                    }
                                    else {
                                        subbr.append($("<td>").text(value[reg_index][subdata]))
                                    }
                                }
                                subb.append(subbr)
                            }
                            subt.append(subh)
                            subt.append(subb)
                            tr.append($('<td>').append(subt))
                        }
                        else if ($(headers[i]).data('format') == 'ImageField') {
                            if (value){
                                tr.append($('<td>').append($('<img src="'+value+'" height="30%">')));
                            }
                            else{
                                tr.append($('<td>'));
                            }
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
        // }
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
    var order = 'asc'
    var headers = $(table.find('thead tr th'));
    if (table.data().selectable){
        unsortable.push(0)
        sorting = 1
    }
    if ($(headers[sorting]).data('name') == 'date'){
        order = 'desc'
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
        "aaSorting": [[sorting,order]]
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
    var useCache = table.attr("use-cache");
    $('.loading').show()
    if (useCache){
        console.log("Table is set to use cache")
        if (name + "-update" in messages){
            console.log("New tsp of "+name+"-update was found in messages: "+messages[name + "-update"])
            var oldupdate = sessionStorage.getItem(name + "-update")
            console.log("Comparing to old tsp: "+oldupdate)
            if (oldupdate && (oldupdate < messages[name + "-update"])) {
                console.log("New tsp is older, removing cached table "+name+" from store")
                sessionStorage.removeItem(name)
            }
            else{
                console.log("Old tsp seems to be the latest update")
            }
            sessionStorage.setItem(name + "-update", messages[name + "-update"]);
        }
        else{
            var d = new Date().getTime()+""
            console.log("Tsp was not received, generating a new one: "+d)
            sessionStorage.setItem(name + "-update", d);
        }
    }
    if (!sessionStorage.getItem(name) || !useCache){
        if (!useCache) {
            console.log("Table don't use cache. Fetching")
        }
        else if (!sessionStorage.getItem(name)) {
            console.log("Cached table was not found in store. Fetching")
        }
        $.get( window.location.origin + table.data().rest, function( data ) {
            if (useCache){
                console.log("Storing table in cache")
                sessionStorage.setItem(name, JSON.stringify(data));
            }
            build_table(table, data)
            $('.loading').hide()
        });
        console.log("Fetched table data");
    }
    else{
        console.log("Using cached data");
        build_table(table, JSON.parse(sessionStorage.getItem(name)))
        $('.loading').hide()
    }
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var data = $(this).closest('tr').data()
    var editform = $("#edit form");
    editform[0].reset();
    editform.trigger("reset");
    editform.find('select').each(function (){
        $(this).val("");
    });
    for (key in data){
        var value = data[key]
        if (key == "date"){
            if (value.length == 10){
                value += " 00:00"
            }
            var d = new Date(value);
            if (editform.find('input[name="'+ key +'"]').attr('type') == "datetime-local"){
                value = d.getFullYear()+"-"+("0"+(d.getMonth()+1)).slice(-2)+"-"+("0"+d.getDate()).slice(-2)+"T"+("0"+d.getHours()).slice(-2)+":"+("0"+d.getMinutes()).slice(-2)+":"+("0"+d.getSeconds()).slice(-2);
            }
            else{
                value = d.getFullYear()+"-"+("0"+(d.getMonth()+1)).slice(-2)+"-"+("0"+d.getDate()).slice(-2);
            }
        } else if (typeof(data[key]) == "object"){
            if (data[key]){
                value = JSON.stringify(data[key]);
            }
            else{
                value = ""
            }
        }
        editform.find('input[name="'+ key +'"]').val(value);
        var field = editform.find('input[name="'+ key +'"]')
        if (field.attr("type") == "checkbox"){
            if (value == "Si" || value == "True" || value === true){
                field.prop('checked', true);
            }else {
                field.prop('checked', false);
            }
        }
        var selected = ''
        editform.find('select[name="'+ key +'"] option').each(function (){
            if ($(this).val() == data[key]){
                selected = $(this).val()
            }
        })
        editform.find('select[name="'+ key +'"]').val(selected);
        editform.find('input[type="checkbox"]').each(function () {
            $(this).val("Si")
        });
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
