document.addEventListener("DOMContentLoaded", () => {
    fetchWeather();
    fetchTests();
});

// -------------------------------
// Hent værdata fra /weather og vis det
// -------------------------------
function fetchWeather(date = null) { // mangler feilhåndtering på filter men men
    let url = "/weather";
    if (date) {
        url += `?date=${date}`
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // console.log("Værdata mottatt:", data);
            updateWeatherTable(data);
            updateChart(data);
        })
        .catch(error => console.error("Feil ved henting av værdata:", error));
}

// -------------------------------
// Send ny temperaturmåling til /add-temperature
// -------------------------------
function createWeather() {
    const date = document.getElementById("dateInput").value;
    const temperature = document.getElementById("tempInput").value;

    fetch("/weather", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date: date, temperature: temperature })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Temperatur lagret:", data);
            fetchWeather(); // Oppdater visning og graf
        })
        .catch(error => console.error("Feil ved sending av temperatur:", error));
}

// -------------------------------
// Hent testdata fra /test med en GET-request skriv dataen til konsollen
// -------------------------------
function fetchTests() {
    fetch("/tests")
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => console.error("Feil ved henting av testdata:", error));
}

// -------------------------------
// Send testdata til /send-test-data med en POST-request
// -------------------------------
function createTest() {
    const header = "overskrift";
    const message = "her skriver jeg teksten";

    fetch("/tests", {
        method: "POST", // Her må vi definere POST. Hvis vi ikke skriver method blir det automatisk GET.
        headers: { "Content-Type": "application/json" }, // Når vi sender data må vi også definere 'headers' som sier noe om hva slags data vi sender
        body: JSON.stringify({ header: header, message: message }) // Selve dataen
    })
        .then(response => response.json())
        .then(data => {
            console.log("Testdata lagret. Kjør fetchTestData() for å se dataen.");
        })
        .catch(error => console.error("Feil ved sending av testdata:", error));
}

// -------------------------------
// Oppgave 2a:
// -------------------------------
function fetchExamples() {
    fetch("/examples") // Ber serveren (app.py) om data via endepunktet /example-data
        .then(response => response.json()) // Konverter responsen til JSON
        .then(data => {
            console.log("Mottatt data:", data); // Logg data til konsollen
        })
        .catch(error => console.error("Feil ved henting av data:", error)); // Viser feilmelding i konsollen hvis vi ikke får data.
}

// -------------------------------
// Oppdater værdata-tabellen i HTML
// -------------------------------
function updateWeatherTable(data) {
    const tableBody = document.getElementById("weatherTableBody");
    tableBody.innerHTML = ""; // Tøm tabellen før oppdatering

    data.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${item.date}</td><td>${item.temperature}°C</td>`;
        tableBody.appendChild(row);
    });
}

// -------------------------------
// Initialiser en tom graf med Chart.js
// -------------------------------
let weatherChart;
function setupChart() {
    const ctx = document.getElementById("weatherChart").getContext("2d");
    weatherChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: [],
            datasets: [{
                label: "Temperatur",
                data: [],
                backgroundColor: "rgba(75, 192, 192, 0.6)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// -------------------------------
// Oppdater Chart.js-grafen med nye værdata
// -------------------------------
function updateChart(data) {
    if (!weatherChart) {
        setupChart();
    }

    weatherChart.data.labels = data.map(item => item.date);
    weatherChart.data.datasets[0].data = data.map(item => item.temperature);
    weatherChart.update();
}