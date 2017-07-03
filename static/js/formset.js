function refreshFormSetInputs(form) {
    var valueSet = []
    form.find('input.formset').each(function () {
        var inputSet = $(this);
        var modelName = inputSet.data('model');
        form.find('#'+modelName+'FormSet-table tbody tr').each(function () {
            var itemData = $(this).data();
            valueSet.push(itemData);
        });
        inputSet.val(JSON.stringify(valueSet));
    });
}

function initialFormSetData(form, modelName, data) {
    var headers = []
    form.find('#'+modelName+'FormSet-table thead th').each(function () {
        if ($(this).data("field")){
            headers.push($(this).data("field"));
        }
    });
    var body = form.find('#'+modelName+'FormSet-table tbody')
    body.empty()
    for (index in data){
        var row = $('<tr>')
        for (field in headers){
            var text = data[index][headers[field]] || "";
            row.attr("data-"+headers[field], text);
            row.append("<td>"+text+"</td>");
        }
        row.attr("data-id", data[index].id);
        row.append('<td><button type="buttton" class="btn btn-sm btn-success '+modelName+'FormSet-edit"><i class="fa fa-pencil"></i></button></td>');
        if (form.find('#'+modelName+'FormSet-table').attr('data-allow_create')){
            row.append('<td><button type="buttton" class="btn btn-sm btn-danger '+modelName+'FormSet-delete"><i class="fa fa-trash"></i></button></td>');
        }
        body.append(row)
    }
    refreshFormSetInputs(form);
}

$(document).on('click', '.'+formSetModelName+'FormSet-edit', function() {
    var data = $(this).closest('tr').data()
    var form = $('#'+formSetModelName+'FormSet-form form')
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
            var d = new Date(data[key]);
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
            if (value == "Si"){
                field.prop('checked', true);
            }else {
                field.prop('checked', false);
            }
        }
        var selected = ''
        form.find('select[name="'+ key +'"] option').each(function (){
            if ($(this).val() == data[key]){
                selected = $(this).val()
            }
        })
        form.find('select[name="'+ key +'"]').val(selected);
    }
    $('#'+formSetModelName+'FormSet-form').modal('show');
    return false;
});

$(document).on('click', '.'+formSetModelName+'FormSet-delete', function() {
    var thisForm = $(this).closest('form');
    $(this).closest('tr').remove();
    refreshFormSetInputs(thisForm);
    return false;
});

$(document).on('click', '.'+formSetModelName+'FormSet-create', function() {
    var form = $('#'+formSetModelName+'FormSet-form form');
    form.trigger("reset");
    form.find('input[type="hidden"]').each(function() {
        $(this).val("");
    });
    form.attr("data-modal", $(this).closest('.modal').attr("id"));
    form.data("modal", $(this).closest('.modal').attr("id"));
    $('#'+formSetModelName+'FormSet-form').modal('show');
    return false;
});

$(document).on('click', 'button[data-target="#edit"]', function () {
    var form = $("#edit form");
    var value = form.find('input#'+formSetInputSetId).val()
    if (value){
        initialFormSetData(form, formSetModelName, JSON.parse(value))
    }
    return false;
});

var htmlForm = ""
for (field in formsetFields){
    htmlForm += `<div class="form-group">
             <label for="`+formsetFields[field][0]+`" class="col-sm-2 control-label">`+formsetFields[field][1]+`</label>
             <div class="col-sm-10">`+formsetFields[field][2]+`</div>
         </div>`
}

$('body').append(`<div id="`+formSetModelName+`FormSet-form" class="modal fade" role="dialog">
    <div class="modal-dialog">
    <div class="modal-content">
  <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title">`+formSetModelName+`</h4>
  </div>
  <div class="modal-body">
      <form class="form-horizontal">`+htmlForm+`</form></div>
  <div class="modal-footer">
    <button type="button" data-dismiss="modal" class="btn">Close</button>
    <button type="button" class="btn btn-primary" id="`+formSetModelName+`FormSet-ok">Ok</button>
  </div>
</div>
</div>
</div>`)

$('div.form-group input').each(function(){
    if ($(this).attr("type")!="checkbox" && $(this).attr("type")!="radio"){
        $(this).addClass("form-control")
    }
});
$('div.form-group select').each(function(){
	$(this).addClass("form-control")
});

$('#'+formSetModelName+'FormSet-form form div.form-group input[type="checkbox"]').change(function(){
    if ($(this).is(':checked')){
        $(this).val("Si")
    }
    else {
        $(this).val("No")
    }
});

$(document).on('click', 'button#'+formSetModelName+"FormSet-ok", function(){
    var serialized = $('#'+formSetModelName+'FormSet-form form').serializeArray();
    var data = {}
    for (field in serialized){
        data[serialized[field].name] = serialized[field].value
    }
    var modalId = $('#'+formSetModelName+'FormSet-form form').data("modal");
    var form = $("#"+modalId+" form");
    var headers = []
    form.find('#'+formSetModelName+'FormSet-table thead th').each(function () {
        if ($(this).data("field")){
            headers.push($(this).data("field"));
        }
    });
    var oldData = $('#'+formSetModelName+'FormSet-form form').data("old");
    if (oldData){
        oldData = JSON.parse(oldData)
    }
    if (oldData){
        form.find('#'+formSetModelName+'FormSet-table tbody tr').each(function(){
            var row = $(this);
            if (JSON.stringify(oldData) == JSON.stringify(row.data())){
                for (field in headers) {
                    var text = data[headers[field]] || "";
                    row.attr("data-"+headers[field], text);
                    row.data(headers[field], text);
                    $(row.children()[field]).text(text);
                }
            }
        });
    }
    else {
        var row = $("<tr>");
        for (field in headers){
            var text = data[headers[field]] || "";
            row.attr("data-"+headers[field], text);
            row.data(headers[field], text);
            row.append("<td>"+text+"</td>");
        }
        row.append('<td><button type="buttton" class="btn btn-sm btn-success '+formSetModelName+'FormSet-edit"><i class="fa fa-pencil"></i></button></td>');
        if (form.find('#'+formSetModelName+'FormSet-table').attr('data-allow_create')){
            row.append('<td><button type="buttton" class="btn btn-sm btn-danger '+formSetModelName+'FormSet-delete"><i class="fa fa-trash"></i></button></td>');
        }
        form.find('#'+formSetModelName+'FormSet-table').append(row);
    }
    $('#'+formSetModelName+'FormSet-form form').removeAttr("data-modal");
    $('#'+formSetModelName+'FormSet-form form').data("modal", "");
    $('#'+formSetModelName+'FormSet-form form').removeAttr("data-old");
    $('#'+formSetModelName+'FormSet-form form').data("old", "");
    $('#'+formSetModelName+'FormSet-form').modal('hide');
    refreshFormSetInputs(form);
    return false;
});
