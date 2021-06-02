$(document).on('click', 'button[data-target="#edit"]', function () {
    editEvent(null, null, $(this).closest('tr').data());
});
$(document).on('click', 'button[data-target="#delete"]', function () {
    deleteEvent(null, null, $(this).closest('tr').data());
});