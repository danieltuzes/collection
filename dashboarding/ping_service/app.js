let interval;
let chart;
let latencyData = [];

function startMeasuring() {
    interval = setInterval(measureLatency, 1000);
}

function stopMeasuring() {
    clearInterval(interval);
}

async function measureLatency() {
    const start = performance.now();
    const response = await fetch('/ping');
    const end = performance.now();
    const rtt = end - start;

    const serverTime = await response.text();
    document.getElementById("latencyData").innerHTML += `${rtt.toFixed(2)} ms (at ${serverTime})<br/>`;

    // Send the measured latency to the server
    await fetch('/store_latency', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            rtt: rtt.toFixed(2),
            serverTime: serverTime
        })
    });

    // Append to local data and update chart
    latencyData.push({time: serverTime, value: rtt});
    updateChart();
}


async function downloadLatencyData() {
    window.location = '/download';
}

function updateChart() {
    const ctx = document.getElementById('latencyChart').getContext('2d');
    if (chart) {
        chart.destroy();
    }
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: latencyData.map(d => d.time),
            datasets: [{
                label: 'Latency (ms)',
                data: latencyData.map(d => d.value),
                borderColor: 'blue',
                lineTension: 0,  // Connect dots with straight lines
                fill: false
            }]
        },
        options: {
            animation: {
                duration: 0
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'series',
                    time: {
                        parser: 'HH:mm:ss',
                        unit: 'minute',
                        displayFormats: {
                            minute: 'HH:mm'
                        }
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        min: 0  // Set the minimum value of y-axis to 0
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Latency (ms)'
                    }
                }]
            }
        }
    });
}

function downloadChart() {
    const a = document.createElement('a');
    a.href = chart.toBase64Image();
    a.download = 'chart.png';
    a.click();
}

(async function getServerLocation() {
    const location = await fetch('/location').then(res => res.text());
    document.getElementById('serverLocation').innerText = location;
})();
