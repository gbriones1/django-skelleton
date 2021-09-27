var inputsData = []
var providers = []
var providerNames = {}

for (var idx in dateRanges){
    var startDate = dateRanges[idx][0]
    var text = startDate.getDate()+" "+monthNames[startDate.getMonth()]
    $('#weekSelect').append('<option value="'+idx+'">'+text+'</option>'); 
}

$("#weekSelect option:last").attr("selected", "selected");


function buildTables(){
    $('#providersInputTable').bootstrapTable({
        columns: [{
            field: 'date',
            title: 'Fecha',
            sortable: true,
            filterControl: 'input'
        },{
            field: 'product_name',
            title: 'Refaccion',
            sortable: true,
            filterControl: 'input',
        },{
            field: 'price',
            title: 'Total',
            sortable: true,
            filterControl: 'input',
        },{
            field: 'amount',
            title: 'Cantidad',
            sortable: true,
            filterControl: 'input',
        },{
            field: 'total',
            title: 'Total',
            sortable: true,
            filterControl: 'input',
        }],
        filterControl: true,
        showFooter: true,
        showExport: true,
        toolbar: "#providersToolbar"
    })
    updateTables($('#weekSelect').val())
}

function updateTables(rangeIdx) {
    providerInputsData = []
    $('#providersInputTable').bootstrapTable('load', providerInputsData)
}

$.when(getObjectDateRange("input", formatDate(start), formatDate(end), function (data){
    inputsData = data
}), getObject("provider")).done(function (){
    providers = JSON.parse(sessionStorage.getItem("provider") || "[]")
    for (provider of providers){
        providerNames[provider.id] = provider.name
    }
    $(document).on("change", "#weekSelect", function(){
        updateTables($(this).val())
    });
    buildTables()
})