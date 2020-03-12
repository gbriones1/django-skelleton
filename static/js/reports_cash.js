var collectionsData = []
var paymentsData = []
var cashData = []

for (var idx in dateRanges){
    var startDate = dateRanges[idx][0]
    var text = startDate.getDate()+" "+monthNames[startDate.getMonth()]
    $('#weekSelect').append('<option value="'+idx+'">'+text+'</option>'); 
}

$("#weekSelect option:last").attr("selected", "selected");

function buildTables(){
    $('#cashTable').bootstrapTable({
        columns: [{
            field: 'date',
            title: 'Fecha',
        },{
            field: 'in',
            title: 'Entrada',
        },{
            field: 'out',
            title: 'Salida',
        },{
            field: 'balance',
            title: 'Balance',
        }],
        showFooter: true,
    })
    updateTables($('#weekSelect').val());
}

function updateTables(rangeIdx) {
    var tableData = []
    var balance = 0;
    for (cash of cashData){
        var cashDate = new Date(cash.date+"T00:00:00")
        if (cashDate >= dateRanges[rangeIdx][0] && cashDate <= dateRanges[rangeIdx][1]){
            if (cash.in){
                balance += cash.in
            }
            if (cash.out){
                balance += cash.out
            }
            tableData.push({
                date: cash.date,
                "in": cash.in,
                "out": cash.out,
                balance: balance
            })
        }
    }
    $('#cashTable').bootstrapTable('load', tableData)
}

$.when(getObjectDateRange("collection", formatDate(start), formatDate(end), function (data){
    collectionsData = data
}), getObjectDateRange("payment", formatDate(start), formatDate(end), function (data){
    paymentsData = data
})).done(function (){
    data = []
    for (collection of collectionsData){
        if (collection.method == 'C'){
            data.push({
                date: collection.date,
                "in": parseFloat(collection.amount),
                "out": null,
            })
        }
    }
    for (payment of paymentsData){
        if (payment.method == 'C'){
            data.push({
                date: payment.date,
                "in": null,
                "out": -parseFloat(payment.amount),
            })
        }
    }
    data.sort((a, b) => (a.date > b.date) ? 1 : -1)
    cashData = data
    $(document).on("change", "#weekSelect", function(){
        updateTables($(this).val())
    });
    buildTables()
});