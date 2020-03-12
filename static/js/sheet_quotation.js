function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}
function startsWith(str, suffix) {
    return str.indexOf(suffix) === 0;
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

function getObject(name, origin){
    object = sessionStorage.getItem(name)
    if (object){
        return function (param) {
            _mockAjaxOptions = param;
            param.complete("data", "textStatus", "jqXHR");
        }
    } else {
        console.log(name+" not cached")
        return $.ajax({
            url: origin+'/database/api/'+name+"/",
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

$('.sheet').each(function () {
    var sheet = $(this);
    var origin = $(this).attr("origin");
    var url = origin+$(this).attr("use_rest")+$(this).attr("data-obj_id")+"/";
    var headSection = $(this).find(".sheet-head")
    var descSection = $(this).find(".sheet-desc");
    var contSection = $(this).find(".sheet-cont");
    var contFields = contSection.data().fields;
    var descFields = descSection.data().fields;
    $.when(getObject("product", origin), getObject("customer", origin)).done(function (){
        var products = JSON.parse(sessionStorage.getItem("product") || "[]")
        var customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
        var productNames = {}
        products.forEach(function (item, index) {
            productNames[item.id] = item.code + " - " + item.name + " - " + item.description
        });
        var customerNames = {}
        customers.forEach(function (item, index) {
            customerNames[item.id] = item.name
        });
        $.getJSON(url, function (data) {
            data.customer_name = customerNames[data.customer]
            headSection.find(".folio").text(data.id);
            headSection.find(".date").text(data.date);
            for (var field in descFields){
                if (data[field]){
                    descSection.append('<div class="col-xs-4" style="padding: 0;"><table class="table table-striped" style="border: solid;border-width: 2px;border-color: #f9f9f9;margin: 0;"><tr><th>'+descFields[field].label+'</th></tr><tr><td>'+data[field]+'</td></tr></table></div>');
                }
            }
            var total = 0.0
            for (field in contFields){
                var price = 0.0;
                var amount = 1;
                var name = ''
                if (endsWith(field, 'product_set')){
                    for (p in data[field]){
                        name = productNames[data[field][p].product]
                        price = parseFloat(data[field][p].price);
                        amount = parseInt(data[field][p].amount);
                        total += price*amount
                        contSection.find('tbody').append('<tr><td>'+name+'</td><td class="right">$'+price.toFixed(2)+'</td><td>'+amount+'</td><td class="right">$'+(price*amount).toFixed(2)+'</td></tr>')
                    }
                }
                else if (endsWith(field, "others_set")) {
                    for (p in data[field]){
                        name = data[field][p].description;
                        price = parseFloat(data[field][p].price);
                        amount = parseInt(data[field][p].amount);
                        total += price*amount
                        contSection.find('tbody').append('<tr><td>'+name+'</td><td class="right">$'+price+'</td><td>'+amount+'</td><td class="right">$'+(price*amount).toFixed(2)+'</td></tr>')
                    }
                }
                else {
                    price = parseFloat(data[field]);
                    if (price){
                        name = contFields[field].label;
                        amount = 1;
                        if (field == 'discount'){
                            amount = -1;
                        }
                        total += price*amount;
                        contSection.find('tbody').append('<tr><td>'+name+'</td><td class="right">$'+price.toFixed(2)+'</td><td>'+amount+'</td><td class="right">$'+(price*amount).toFixed(2)+'</td></tr>')
                    }
                }

            }
            contSection.find(".total").text("$"+total.toFixed(2));
            for (field in data){
                if (startsWith(field, "unit_section_")){
                    if (data[field]){
                        $('#'+field).show()
                    }
                }
            }
        });
    });
});
