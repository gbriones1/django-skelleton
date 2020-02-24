var salesData = []
var collectionsData = []
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

function buildTables(){
    $('#salesTable').bootstrapTable({
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
        showExport: true,
        toolbar: "#salesToolbar"
    })
    $('#collectionsTable').bootstrapTable({
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
            field: 'amount',
            title: 'Cantidad',
            sortable: true,
            filterControl: 'input',
            footerFormatter: totalPriceFormatter
        },{
            field: 'method_name',
            title: 'Forma de pago',
            sortable: true,
            filterControl: 'select'
        }],
        filterControl: true,
        showFooter: true,
        showExport: true,
        toolbar: "#collectionsToolbar"
    })
    updateTables($('#weekSelect').val())
}

function updateTables(rangeIdx) {
    salesTableData = []
    collectionsTableData = []
    for (sell of salesData){
        var sellDate = new Date(sell.date+"T00:00:00")
        if (sellDate >= dateRanges[rangeIdx][0] && sellDate <= dateRanges[rangeIdx][1]){
            salesTableData.push(sell)
            Array.prototype.push.apply(collectionsTableData, sell.collection_set)
        }
    }
    $('#salesTable').bootstrapTable('load', salesTableData)
    $('#collectionsTable').bootstrapTable('load', collectionsTableData)
}

$.when(getObjectDateRange("sell", formatDate(start), formatDate(end), function (data){
    salesData = data
}), getObject("customer")).done(function (){
    customers = JSON.parse(sessionStorage.getItem("customer") || "[]")
    for (customer of customers){
        customerNames[customer.id] = customer.name
    }
    for (sell of salesData){
        sell.customer_name = customerNames[sell.customer]
        sell.collected = 0
        for (collection of sell.collection_set){
            sell.collected += parseFloat(collection.amount)
            collection.customer_name = sell.customer_name
            switch(collection.method) {
                case "C":
                    collection.method_name = "Efectivo"
                    break;
                case "T":
                    collection.method_name = "Transferencia"
                    break;
                case "K":
                    collection.method_name = "Cheque"
                    break;
            }
        }
        sell.debt = sell.price - sell.collected
        sell.debt = sell.debt.toFixed(2)
        sell.collected = sell.collected.toFixed(2)
        sell.invoiced_status = "No"
        if (sell.invoiced){
            sell.invoiced_status = "Si"
        }
    }
    $(document).on("change", "#weekSelect", function(){
        updateTables($(this).val())
    });
    buildTables()
})