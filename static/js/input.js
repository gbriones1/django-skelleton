$('div.modal form button[type="submit"]').each(function () {
    $(this).attr("type", "button")
    $(this).addClass("evaluator")
})

$(document).on('click', 'div.modal form button.evaluator', function () {
    var products = JSON.parse($(this).closest('form').find('input#id_products').val())
    var confirmTable = $('<table>')
    $('#ProductMultiSet-confirm .modal-body table').remove()
    for (i in products){
        var product = $(this).closest('form').find('#ProductMultiSet-table tr[data-id="'+products[i].id+'"]').data()
        confirmTable.append('<tr><td>'+product.code+" - "+product.name+' - '+product.description+'</td><td><input type="number" class="form-control user-success" value="'+product.price+'"></td></tr>')
    }
    $('#ProductMultiSet-confirm .modal-body').append(confirmTable)
    $('#ProductMultiSet-confirm').modal('show');
    return false
});

$(document).on('hidden.bs.modal', '#ProductMultiSet-confirm', function(){
    $('div#new.modal form button[type="submit"]').removeAttr('disabled');
    return false;
});

$(document).on('click', '#ProductMultiSet-evaluate', function(){
    console.log("Evaluating");
    return false;
});

$('body').append(`<div id="ProductMultiSet-confirm" class="modal fade"  role="dialog">
    <div class="modal-dialog">
    <div class="modal-content">
  <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title">Confirmar precios</h4>
  </div>
  <div class="modal-body">
  <table>
  </table>
  </div>
  <div class="modal-footer">
    <button type="button" data-dismiss="modal" class="btn">Close</button>
    <button type="button" class="btn btn-primary" id="ProductMultiSet-evaluate">Ok</button>
  </div>
</div>
</div>
</div>`)
