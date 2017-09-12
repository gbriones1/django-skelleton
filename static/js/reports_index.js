$(document).on('click', 'button[data-target="#view"]', function () {
    var target = $(this).closest('tr').data().report;
    window.location = '/database/reports/'+target
    console.log(target);
});
