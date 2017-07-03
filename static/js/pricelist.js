$('input.multiset').each(function () {
    $(this).closest('form').find('#ProductMultiSet-table tbody tr').each( function () {
        $(this).attr("data-base_price", $(this).attr("data-price"));
    })
});

$(document).on('change', 'select#id_base_price', function(){
    var percentageName = $(this).val()
    var percentagesDef = JSON.parse($(this).closest('form').find('input#id_percentages').val())
    $(this).closest('form').find('#ProductMultiSet-table tbody tr').each(function () {
        var basePrice = parseFloat($(this).attr("data-base_price"));
        var percentage = 0
        if (percentageName){
            for (index in percentagesDef){
                var max_price_limit = parseFloat(percentagesDef[index].max_price_limit)
                if (basePrice <= max_price_limit){
                    percentage = parseFloat(percentagesDef[index][percentageName])
                    break;
                }
            }
        }
        $(this).attr("data-price", (basePrice + (basePrice * percentage / 100)).toFixed(2));
    })
});
