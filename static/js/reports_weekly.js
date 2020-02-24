var salesData = []
var customers = []
var customerNames = {}

for (var idx in dateRanges){
    var startDate = dateRanges[idx][0]
    var text = startDate.getDate()+" "+monthNames[startDate.getMonth()]
    $('#weekSelect').append('<option value="'+idx+'">'+text+'</option>'); 
}

$("#weekSelect option:last").attr("selected", "selected");

function totalPriceFormatter(data) {
    var field = this.field
    return '$' + data.map(function (row) {
        return +row[field]
    }).reduce(function (sum, i) {
        return sum + i
    }, 0).toFixed(2)
}

function buildTable(){
    $('#reportsTable').bootstrapTable({
        columns: [{
            field: 'customer_name',
            title: 'Cliente',
            sortable: true,
            filterControl: 'select'
        },{
            field: 'date',
            title: 'Fecha',
            sortable: true,
            filterControl: 'input'
        },{
            field: 'price',
            title: 'Total',
            sortable: true,
            filterControl: 'input',
            footerFormatter: totalPriceFormatter
        },{
            field: 'collected',
            title: 'Pagado',
            sortable: true,
            filterControl: 'input',
            footerFormatter: totalPriceFormatter
        },{
            field: 'debt',
            title: 'Deuda',
            sortable: true,
            filterControl: 'input',
            footerFormatter: totalPriceFormatter
        },{
            field: 'invoiced_status',
            title: 'Facturado',
            sortable: true,
            filterControl: 'select'
        }],
        filterControl: true,
        showFooter: true,
    })
    updateTable($('#weekSelect').val())
}

function updateTable(rangeIdx) {
    data = []
    for (sell of salesData){
        var sellDate = new Date(sell.date+"T00:00:00")
        if (sellDate >= dateRanges[rangeIdx][0] && sellDate <= dateRanges[rangeIdx][1]){
            data.push(sell)
        }
    }
    $('#reportsTable').bootstrapTable('load', data)
}

$.when(getObjectDateRange("sell", formatDate(start), formatDate(end), function (data){
    salesData = data
}), getObject("customer")).done(function (){
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    for (customer of customers){
        customerNames[customer.id] = customer.name
    }
    for (sell of salesData){
        sell.collected = 0
        for (collection of sell.collection_set){
            sell.collected += parseFloat(collection.amount)
        }
        sell.debt = sell.price - sell.collected
        sell.debt = sell.debt.toFixed(2)
        sell.collected = sell.collected.toFixed(2)
        sell.invoiced_status = "No"
        if (sell.invoiced){
            sell.invoiced_status = "Si"
        }
        sell.customer_name = customerNames[sell.customer]
    }
    $(document).on("change", "#weekSelect", function(){
        updateTable($(this).val())
    });
    buildTable()
})