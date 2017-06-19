function loadChart(data){
    var config = {
    type: 'line',
    data: {
        labels: ["9min ago", "8min ago", "7min ago", "6min ago", "5min ago", "4min ago", "3min ago", "2min ago" ,"1min ago","0min ago"],
        datasets: [{
            label: "humidity",
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            data: data,
            fill: false
        }]
    },
    options: {
        animation: false,
        responsive: true,
        title: {
            display: true,
            text: 'humidity zone 1'
        },
        tooltips: {
            mode: 'index',
            intersect: false
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Time (minutes)'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Humidity (%)'
                }
            }]
        }
    }
};
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
}