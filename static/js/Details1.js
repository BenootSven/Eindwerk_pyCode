function loadChart(data) {
    var config = {
        type: 'line',
        data: {
            labels: ["9min geleden", "8min geleden", "7min geleden", "6min geleden", "5min geleden", "4min geleden", "3min geleden", "2min geleden" ,"1min geleden","0min geleden"],
            datasets: [{
                label: "temperatuur",
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
                text: 'temperatuur binnen'
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
                        labelString: 'Tijd (minuten)'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Graden (°C)'
                    }
                }]
            }
        }
    };
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);

}