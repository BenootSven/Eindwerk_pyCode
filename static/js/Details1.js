function loadChart(data) {
    var config = {
        type: 'line',
        data: {
            labels: ["9min ago", "8min ago", "7min ago", "6min ago", "5min ago", "4min ago", "3min ago", "2min ago" ,"1min ago","0min ago"],
            datasets: [{
                label: "temperature",
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
                text: 'temperature inside'
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
                        labelString: 'Degrees (°C)'
                    }
                }]
            }
        }
    };
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);

}