$(document).on('click', 'button[data-target="#edit"]', function () {
    var data = $(this).closest('tr').data()
    var inputform = $("#edit form");
    for (opIndx in data.movement_product_set){
        var opData = inputform.find("input#id_movement_product_set").closest(".multiSet-container").find('#multiSet-table tbody tr[data-id='+data.movement_product_set[opIndx].product.id+']').data();
        data.movement_product_set[opIndx].price = opData.price
        data.movement_product_set[opIndx].discount = opData.discount
    }
    initialMultiSetData(inputform.find("input#id_movement_product_set"), data.movement_product_set);
    refreshMutliSetInputs(inputform);
});
