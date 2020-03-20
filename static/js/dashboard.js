TRANSLATIONS = {
    'name': 'nombre',
    'provider': 'Proveedor',
    'date': "Fecha",
    'amount': "Cantidad",
    'unit': "Unidad",
    'plates': "Placas",
    'customer_name': "Cliente",
    'customer': "Cliente",
    'service': "Servicio",
    'discount': "Descuento",
    'authorized': "Autorizado",
    'work_sheet': "Hoja de Trabajo",
    'organization_storage': 'Almacen',
    'number': 'Numero',
    'This field is required.': 'Este campo no puede estar vacio',
    'This field may not be blank.': 'Este campo no puede estar vacio',
    'This field may not be null.': 'Este campo no puede estar vacio',
}

function getObject(name){
    object = sessionStorage.getItem(name)
    if (object){
        console.log(name+" cached")
        return function (param) {
            _mockAjaxOptions = param;
            param.complete("data", "textStatus", "jqXHR");
        }
    } else {
        console.log(name+" not cached")
        return $.ajax({
            url: '/database/api/'+name+"/",
            type: "GET",
            success: function (data) {
                sessionStorage.setItem(name, JSON.stringify(data))
            },
            error: function (data) {
                handleErrorAlerts(data)
            }
        })
    }
}

function getObjectFiltered(name, success) {
    return $.ajax({
        url: '/database/api/'+name+'/'+window.location.search,
        type: "GET",
        success: success,
        error: function (data) {
            handleErrorAlerts(data)
        }
    })
}

function handleErrorAlerts(response) {
    try {
        data = JSON.parse(response.responseText)
    }
    catch (err){
        data = response.responseText
    }
    if (typeof(data) == "object") {
        for (key in data){
            var value = data[key]
            var field = TRANSLATIONS[key]
            if (field == undefined){
                field = key
            }
            var reason = TRANSLATIONS[value]
            if (reason == undefined){
                reason = value
            }
            createAlert(reason+": "+field, "danger")
        }
    }
    else{
        createAlert(data, "danger")
    }
}

function actionFormatter(value, row, index, field){
    var actionBtns = ''
    actions.forEach(function (item){
        actionBtns += '<button type="button" class="btn btn-'+item.style+' '+item.name+'" data-toggle="'+item.action+'" data-target="#'+item.name+'"><i class="fa fa-'+item.icon+'"></i></button>'
    })
    return actionBtns
}

function editEvent (e, value, data, index) {
    var editform = $("#edit form");
    editform.submit(function() {
        return false;
    });
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
        var field = editform.find('input[name="'+ key +'"]');
        if (field.hasClass('formset')){
            if (typeof initialFormSetData !== 'undefined'){
                initialFormSetData(field, data[key])
            }
        }
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
            $(this).val(true)
        });
    }
}

function deleteEvent (e, value, data, index) {
    var deleteform = $("#delete form");
    deleteform .submit(function() {
        return false;
    });
    deleteform[0].reset();
    deleteform.find('input[name="id"]').val(data['id']);
}

$(document).on('click', 'button.do-new', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form')
    $.ajax({
        url: form.attr("action"),
        data: new URLSearchParams(new FormData(form.get(0))).toString(),
        type: form.attr("method"),
        success: function (data) {
            if (typeof prefetch !== "undefined"){
                prefetch.forEach(function(item) {
                    sessionStorage.removeItem(item)
                });
            }
            location.reload();
        },
        error: function (data) {
            button.attr('disabled', false)
            handleErrorAlerts(data)
        }
    });
});

$(document).on('click', 'button.do-edit', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form')
    formData = getFormData(form)
    $.ajax({
        url: form.attr("action")+formData.id+"/",
        data: new FormData(form.get(0)),
        contentType: false,
        processData: false,
        type: form.attr("method"),
        success: function (data) {
            if (typeof prefetch !== "undefined"){
                prefetch.forEach(function(item) {
                    sessionStorage.removeItem(item)
                });
            }
            location.reload();
        },
        error: function (data) {
            button.attr('disabled', false)
            handleErrorAlerts(data)
        }
    });
});

$(document).on('click', 'button.do-delete', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form')
    formData = getFormData(form)
    $.ajax({
        url: form.attr("action")+formData.id+"/",
        data: form.serialize(),
        type: form.attr("method"),
        success: function (data) {
            if (typeof prefetch !== "undefined"){
                prefetch.forEach(function(item) {
                    sessionStorage.removeItem(item)
                });
            }
            location.reload();
        },
        error: function (data) {
            button.attr('disabled', false)
            handleErrorAlerts(data)
        }
    });
});

$(document).on('click', 'button.do-multi-delete', function () {
    var button = $(this)
    button.attr('disabled', true)
    var form = $(this).closest('.modal-content').find('form')
    $("#table").bootstrapTable('getSelections').forEach(function (item, index) {
        $.ajax({
            url: form.attr("action")+item.id+"/",
            type: "DELETE",
            success: function (data) {
                if (typeof prefetch !== "undefined"){
                    prefetch.forEach(function(item) {
                        sessionStorage.removeItem(item)
                    });
                }
                location.reload();
            },
            error: function (data) {
                button.attr('disabled', false)
                handleErrorAlerts(data)
            }
        });
    })
});
