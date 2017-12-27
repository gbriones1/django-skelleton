$('.sheet').each(function () {
    var sheet = $(this);
    var url = $(this).attr("use_rest")+"/"+$(this).attr("data-obj_id")+"/";
    var headSection = $(this).find(".sheet-head")
    var descSection = $(this).find(".sheet-desc");
    var contSection = $(this).find(".sheet-cont");
    var footSection = $(this).find(".sheet-foot");
    var contFields = contSection.data().fields;
    var descFields = descSection.data().fields;
    $.getJSON(url, function (data) {
        console.log(data);
        headSection.find(".folio").text(data.id);
        headSection.find(".date").text(data.date);
        for (var field in descFields){
            descSection.append('<div class="col-xs-4" style="padding: 0;"><table class="table table-striped" style="border: solid;border-width: 2px;border-color: #f9f9f9;margin: 0;"><tr><th>'+descFields[field].label+'</th></tr><tr><td>'+data[field]+'</td></tr></table></div>');
        }
        var total = 0.0
        for (field in contFields){
            var price = 0.0;
            var amount = 1;
            var name = ''
            if (field.endsWith('product_set')){
                for (p in data[field]){
                    name = data[field][p].product.code+" - "+ data[field][p].product.name+ ' - '+data[field][p].product.description
                    price = parseFloat(data[field][p].price);
                    amount = parseInt(data[field][p].amount);
                    total += price*amount
                    contSection.find('tbody').append('<tr><td>'+name+'</td><td>'+price+'</td><td>'+amount+'</td><td>'+(price*amount)+'</td></tr>')
                }
            }
            else {
                price = parseFloat(data[field]);
                if (price){
                    name = contFields[field].label;
                    amount = 1;
                    total += price*amount;
                    contSection.find('tbody').append('<tr><td>'+name+'</td><td>'+price+'</td><td>'+amount+'</td><td>'+(price*amount)+'</td></tr>')
                }
            }

        }
        footSection.find(".total").text("$"+total)
    });
});
