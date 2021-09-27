var weekCut = 6

$.ajax({
    type: "GET",
    url: '/database/api/configuration/',
    async: false,
    success: function (data) {
        weekCut = data[0].week_cut
    },
});

var weekCount = 10
const monthNames = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
  "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
];

var labels = []
var dateRanges = []
var earningsData = []
var collectionsData = []
var spendingsData = []
var paymentsData = []

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

function getObject(name){
    object = sessionStorage.getItem(name)
    if (object){
        console.log(name+" cached")
        return function (param) {
            _mockAjaxOptions = param;
            param.complete("data", "textStatus", "jqXHR");
        }
    } else {
        console.log(name+" not cached")
        return $.ajax({
            url: '/database/api/'+name+"/",
            type: "GET",
            success: function (data) {
                sessionStorage.setItem(name, JSON.stringify(data))
            },
            error: function (data) {
                handleErrorAlerts(data)
            }
        })
    }
}

function formatDate(date){
    return date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()
}

var end = new Date()
end.setDate(end.getDate() -(end.getDay()-weekCut))
end.setHours(23)
end.setMinutes(59)
end.setSeconds(59)
end.setMilliseconds(999)
var start = new Date(end)
start.setDate(start.getDate() - 7*weekCount+1)
start.setHours(0)
start.setMinutes(0)
start.setSeconds(0)
start.setMilliseconds(0)

for (var i = weekCount; i > 0; i--){
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
    dateRanges.push([from, to])
}

console.log(start)
console.log(end)

