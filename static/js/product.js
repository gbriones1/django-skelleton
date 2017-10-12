$(document).on('click', 'button[data-target="#picture"]', function () {
    var data = $(this).closest('tr').data()
    var form = $("#picture form");
    form.find('input[name="id"]').val(data['id']);
});
