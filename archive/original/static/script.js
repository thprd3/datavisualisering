document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("crimeChart")) {
        loadCrimeChart()
    }
    if (document.getElementById("temperatureChart")) {
        loadWeatherCharts()
    }
})

function loadWeatherCharts() {
    fetch("/temperature-data")
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('temperatureChart');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Temperature (*C)',
                        data: data.values,
                        borderWidth: 2
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        })

    fetch("/precipitation-data")
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('precipitationChart');

            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Precipitation (mm)',
                        data: data.values,
                        borderWidth: 2
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

        })
}

function loadCrimeChart() {
    fetch("/crime-chart-data")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.body.innerHTML += `<p style="color: red;">${data.error}</p>`;
                return;
            }

            const ctx = document.getElementById("crimeChart");

            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.labels, // Age groups
                    datasets: [{
                        label: "Number of Crimes",
                        data: data.values, // Crime counts
                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        })
        .catch(error => {
            document.body.innerHTML += `<p style="color: red;">Error loading chart data: ${error}</p>`;
        });
}