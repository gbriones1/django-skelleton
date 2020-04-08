function refreshFormSetInputs(form) {
    var valueSet = []
    form.find('input.formset').each(function () {
        var inputSet = $(this);
        var inputs = $(this).closest('form').find('input.formset-single');
        inputs.remove();
        inputSet.closest('.formSet-container').find('.formSet-table tbody tr').each(function (key, value) {
            var form = inputSet.closest('form');
            $('<input>').attr({
                type: 'hidden',
                class: 'formset-single',
                id: 'id_'+inputSet.attr('name')+'['+key+']',
                name: inputSet.attr('name')+'['+key+']',
                value: JSON.stringify(value.dataset)
            }).appendTo(form);
            var itemData = $(this).data();
            valueSet.push(itemData);
        });
        inputSet.val(JSON.stringify(valueSet));
    });
}

function initialFormSetData(input, data) {
    var headers = []
    var div = input.closest(".formSet-container")
    div.find('.formSet-table thead th').each(function () {
        if ($(this).data("field")){
            headers.push($(this).data("field"));
        }
    });
    var body = div.find('.formSet-table tbody')
    var formSetModelName = div.find('input.formset').data("model")
    var choiceFields = {}
    $('#'+formSetModelName+'-modal').find("form select").each(function (){
        var choiceName = $(this).attr("name")
        choiceFields[choiceName] = {}
        $(this).find('option').each(function (){
            choiceFields[choiceName][$(this).val()] = $(this).text()
        })
    })
    body.empty()
    for (index in data){
        var row = $('<tr>')
        for (field in headers){
            var text = data[index][headers[field]];
            row.attr("data-"+headers[field], text);
            if (text === true){
                text = '<i class="fa fa-check-circle"></i>'
            } else if (text === false) {
                text = ''
            } else if (headers[field] in choiceFields){
                text = choiceFields[headers[field]][text]
            }
            row.append("<td>"+text+"</td>");
        }
        row.attr("data-id", data[index].id);
        row.append('<td><button type="buttton" class="btn btn-sm btn-success formSet-edit"><i class="fa fa-pencil"></i></button></td>');
        if (div.find('.formSet-table').attr('data-allow_create')){
            row.append('<td><button type="buttton" class="btn btn-sm btn-danger formSet-delete"><i class="fa fa-trash"></i></button></td>');
        }
        body.append(row)
    }
    refreshFormSetInputs(input.closest('form'));
}

$(document).on('click', '.formSet-edit', function() {
    var formSetModelName = $(this).closest('.formSet-container').find('input.formset').data("model");
    var modal = $('#'+formSetModelName+'-modal');
    var form = modal.find("form");
    var data = $(this).closest('tr').data()
    form.attr("data-id", data.id);
    form.data("id", data.id);
    form.attr("data-modal", $(this).closest('.modal').attr("id"));
    form.data("modal", $(this).closest('.modal').attr("id"));
    form.attr("data-old", JSON.stringify(data));
    form.data("old", JSON.stringify(data));
    form.trigger("reset");
    form.find('input[type="hidden"]').each(function() {
        $(this).val("");
    });
    for (key in data){
        var value = data[key]
        if (key == "date"){
            if (value.length == 10){
                value += " 00:00"
            }
            var d = new Date(value);
            if (form.find('input[name="'+ key +'"]').attr('type') == "datetime-local"){
                value = d.getFullYear()+"-"+("0"+(d.getMonth()+1)).slice(-2)+"-"+("0"+d.getDate()).slice(-2)+"T"+("0"+d.getHours()).slice(-2)+":"+("0"+d.getMinutes()).slice(-2)+":"+("0"+d.getSeconds()).slice(-2);
            }
            else{
                value = d.getFullYear()+"-"+("0"+(d.getMonth()+1)).slice(-2)+"-"+("0"+d.getDate()).slice(-2);
            }
        } else if (typeof(data[key]) == "object"){
            value = JSON.stringify(data[key]);
        }
        form.find('input[name="'+ key +'"]').val(value);
        var field = form.find('input[name="'+ key +'"]')
        if (field.attr("type") == "checkbox"){
            field.prop('checked', value);
            field.removeAttr("value");
        }
        var selected = ''
        form.find('select[name="'+ key +'"] option').each(function (){
            if ($(this).val() == data[key]){
                selected = $(this).val()
            }
        })
        form.find('select[name="'+ key +'"]').val(selected);
    }
    modal.modal('show');
    return false;
});

$(document).on('click', '.formSet-delete', function() {
    var thisForm = $(this).closest('form');
    $(this).closest('tr').remove();
    refreshFormSetInputs(thisForm);
    return false;
});

$(document).on('click', '.formSet-create', function() {
    var formSetModelName = $(this).closest('.formSet-container').find('input.formset').data("model");
    var modal = $('#'+formSetModelName+'-modal');
    var form = modal.find("form");
    form.trigger("reset");
    form.find('input[type="hidden"]').each(function() {
        $(this).val("");
    });
    form.attr("data-modal", $(this).closest('.modal').attr("id"));
    form.data("modal", $(this).closest('.modal').attr("id"));
    modal.modal('show');
    return false;
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var form = $("#edit form");
    form.find('input.formset').each(function() {
        var value = $(this).val() || "[]"
        if (value){
            value = JSON.parse(value)
        }
        initialFormSetData($(this), value)
    })
});


$('input.formset').each(function () {
    var formSetModelName = $(this).data("model")
    var formsetFields = $(this).data("fields")
    var htmlForm = ""
    for (field in formsetFields){
        htmlForm += '<div class="form-group"><label for="'+formsetFields[field][0]+'" class="col-sm-2 control-label">'+formsetFields[field][1]+'</label><div class="col-sm-10">'+formsetFields[field][2]+'</div></div>'
    }
    $('body').append('<div id="'+formSetModelName+'-modal" class="modal fade formSet-form" role="dialog"><div class="modal-dialog"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal">&times;</button><h4 class="modal-title"></h4></div><div class="modal-body"><form class="form-horizontal">'+htmlForm+'</form></div><div class="modal-footer"><button type="button" data-dismiss="modal" class="btn">Close</button><button type="button" class="btn btn-primary formSet-ok">Ok</button></div></div></div></div>')
})

$('div.form-group input').each(function(){
    if ($(this).attr("type")!="checkbox" && $(this).attr("type")!="radio"){
        $(this).addClass("form-control")
    }
});
$('div.form-group select').each(function(){
	$(this).addClass("form-control")
});

// $('.formSet-form form div.form-group input[type="checkbox"]').change(function(){
//     $(this).val($(this).is(':checked'))
// });

$(document).on('click', 'button.formSet-ok', function(){
    var modal = $(this).closest('.modal')
    var modalForm = modal.find('form')
    var checkboxFields = []
    modalForm.find('input[type="checkbox"]').each(function (){
        checkboxFields.push($(this).attr('name'));
    })
    var formData = new FormData(modalForm.get(0))
    var data = {}
    for (var entry of formData.entries()){
        data[entry[0]] = entry[1]
    }
    var modalId = modalForm.data("modal");
    var form = $("#"+modalId+" form");
    var headers = []
    form.find('.formSet-table thead th').each(function () {
        if ($(this).data("field")){
            headers.push($(this).data("field"));
        }
    });
    var choiceFields = {}
    modalForm.find("select").each(function (){
        var choiceName = $(this).attr("name")
        choiceFields[choiceName] = {}
        $(this).find('option').each(function (){
            choiceFields[choiceName][$(this).val()] = $(this).text()
        })
    })
    var oldData = modalForm.data("old");
    if (oldData){
        oldData = JSON.parse(oldData)
    }
    if (oldData){
        form.find('.formSet-table tbody tr').each(function(){
            var row = $(this);
            if (JSON.stringify(oldData) == JSON.stringify(row.data())){
                for (field in headers) {
                    var text = data[headers[field]];
                    if (checkboxFields.includes(headers[field])){
                        if (text == "on"){
                            text = true
                        }
                        else {
                            text = false
                        }
                    }
                    row.attr("data-"+headers[field], text);
                    row.data(headers[field], text);
                    if (text === true){
                        text = '<i class="fa fa-check-circle"></i>'
                        $(row.children()[field]).html(text);
                    } else if (text === false) {
                        $(row.children()[field]).text("");
                    } else if (headers[field] in choiceFields){
                        $(row.children()[field]).text(choiceFields[headers[field]][text])
                    } else if (typeof text !== 'undefined') {
                        $(row.children()[field]).text(text);
                    }
                }
            }
        });
    }
    else {
        var row = $("<tr>");
        for (field in headers){
            var text = data[headers[field]];
            if (checkboxFields.includes(headers[field])){
                if (text == "on"){
                    text = true
                }
                else{
                    text = false
                }
            }
            row.attr("data-"+headers[field], text);
            row.data(headers[field], text);
            if (text === true){
                text = '<i class="fa fa-check-circle"></i>'
            } else if (text === false) {
                text = ''
            } else if (headers[field] in choiceFields){
                text = choiceFields[headers[field]][text]
            } else if (typeof text == 'undefined') {
                text = ''
            }
            row.append("<td>"+text+"</td>");
        }
        row.append('<td><button type="buttton" class="btn btn-sm btn-success formSet-edit"><i class="fa fa-pencil"></i></button></td>');
        if (form.find('.formSet-table').attr('data-allow_create')){
            row.append('<td><button type="buttton" class="btn btn-sm btn-danger formSet-delete"><i class="fa fa-trash"></i></button></td>');
        }
        form.find('.formSet-table').append(row);
    }
    modalForm.removeAttr("data-modal");
    modalForm.data("modal", "");
    modalForm.removeAttr("data-old");
    modalForm.data("old", "");
    modal.modal('hide');
    refreshFormSetInputs(form);
    // return false;
});

$('input.formset').closest('form').submit(function () {
    var form = $(this).closest("form");
    refreshFormSetInputs(form);
});
