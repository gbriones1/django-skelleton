var weekCut = 4
const monthNames = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
  "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
];

var labels = []
var dateRanges = []
var earningsData = []
var collectionsData = []

function getObjectDateRange(name, from, to, success) {
    return $.ajax({
        url: '/database/api/'+name+'/?date__gte='+from+'&date__lte='+to,
        type: "GET",
        success: success,
        error: function (data) {
            alert(data.responseText)
        }
    })
}

function formatDate(date){
    return date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()
}

var end = new Date()
end.setDate(end.getDate() + 7-(end.getDay()-weekCut))
end.setHours(23)
end.setMinutes(59)
end.setSeconds(59)
end.setMilliseconds(999)
var start = new Date(end)
start.setDate(start.getDate() - 55)
start.setHours(0)
start.setMinutes(0)
start.setSeconds(0)
start.setMilliseconds(0)

for (var i = 7; i >= 0; i--){
    var to = new Date()
    to.setDate(to.getDate() + 7-(to.getDay()-weekCut)-(i*7))
    to.setHours(23)
    to.setMinutes(59)
    to.setSeconds(59)
    to.setMilliseconds(999)
    var from = new Date(to)
    from.setDate(from.getDate() - 6)
    from.setHours(0)
    from.setMinutes(0)
    from.setSeconds(0)
    from.setMilliseconds(0)
    labels.push(from.getDate()+"-"+monthNames[from.getMonth()])
    dateRanges.push([from, to, []])
}

$.when(getObjectDateRange("sell", formatDate(start), formatDate(end), function (data){
    // console.log(data);
    for (sell of data){
        var sellDate = new Date(sell.date+"T00:00:00")
        // console.log(sellDate)
        for (var idx in dateRanges){
            if (sellDate >= dateRanges[idx][0] && sellDate <= dateRanges[idx][1]){
                dateRanges[idx][2].push(sell)
                break;
            }
        }
    }
    // console.log(dateRanges)
    for (idx in dateRanges){
        var total = 0
        var collections = 0
        for (sell of dateRanges[idx][2]){
            total += parseFloat(sell.price)
            for (collection of sell.collection_set){
                collections += parseFloat(collection.amount)
            }
        }
        earningsData.push(total)
        collectionsData.push(collections)
    }
})).done(function (){
    renderChart()
})

function renderChart (){
    var ctx = document.getElementById('earningsChart').getContext('2d');
    var myChart = new Chart(ctx, {
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