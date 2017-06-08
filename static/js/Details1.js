function loadChart(data) {
    var config = {
        type: 'line',
        data: {
            labels: ["00:00", "February", "March", "April", "May", "June", "July", "00:00"],
            datasets: [{
                label: "temp",
                backgroundColor: window.chartColors.red,
                borderColor: window.chartColors.red,
                data: data,
                fill: false
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'temperatuur sensor 1'
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
                        labelString: 'Month'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);

}