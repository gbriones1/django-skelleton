$.when(getObjectDateRange("sell", formatDate(start), formatDate(end), function (data){
    var sellRanges = Array(dateRanges.length).fill(null).map(()=>new Array());;
    for (sell of data){
        var sellDate = new Date(sell.date+"T00:00:00")
        for (var idx in dateRanges){
            if (sellDate >= dateRanges[idx][0] && sellDate <= dateRanges[idx][1]){
                sellRanges[idx].push(sell)
                break;
            }
        }
    }
    for (idx in dateRanges){
        var total = 0
        var collections = 0
        for (sell of sellRanges[idx]){
            total += parseFloat(sell.price)
            for (collection of sell.collection_set){
                collections += parseFloat(collection.amount)
            }
        }
        earningsData.push(total)
        collectionsData.push(collections)
    }
}), getObjectDateRange("invoice", formatDate(start), formatDate(end), function (data){
    var invoiceRanges = Array(dateRanges.length).fill(null).map(()=>new Array());;
    for (invoice of data){
        var buyDate = new Date(invoice.date+"T00:00:00")
        for (var idx in dateRanges){
            if (buyDate >= dateRanges[idx][0] && buyDate <= dateRanges[idx][1]){
                invoiceRanges[idx].push(invoice)
                break;
            }
        }
    }
    for (idx in invoiceRanges){
        var total = 0
        var payments = 0
        for (invoice of invoiceRanges[idx]){
            total += parseFloat(invoice.price)
            for (payment of invoice.payment_set){
                payments += parseFloat(payment.amount)
            }
        }
        spendingsData.push(total)
        paymentsData.push(payments)
    }
})).done(function (){
    renderCharts()
})

function renderCharts (){
    var ctx = document.getElementById('earningsChart').getContext('2d');
    var earningsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ventas teoricas',
                data: earningsData,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Ventas relativa',
                data: collectionsData,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    var ctx = document.getElementById('spendingsChart').getContext('2d');
    var spendingsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Gastos teoricos',
                data: spendingsData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }, {
                label: 'Gastos relativos',
                data: paymentsData,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

// var ctx = document.getElementById('myChart').getContext('2d');
// var myChart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//         labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//         datasets: [{
//             label: '# of Votes',
//             data: [12, 19, 3, 5, 2, 3],
//             backgroundColor: [
//                 'rgba(255, 99, 132, 0.2)',
//                 'rgba(54, 162, 235, 0.2)',
//                 'rgba(255, 206, 86, 0.2)',
//                 'rgba(75, 192, 192, 0.2)',
//                 'rgba(153, 102, 255, 0.2)',
//                 'rgba(255, 159, 64, 0.2)'
//             ],
//             borderColor: [
//                 'rgba(255, 99, 132, 1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)',
//                 'rgba(153, 102, 255, 1)',
//                 'rgba(255, 159, 64, 1)'
//             ],
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     beginAtZero: true
//                 }
//             }]
//         }
//     }
// });