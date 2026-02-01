// voltage per day graph
async function loadVoltageDay() {
    const today = new Date();
    const day = today.toLocaleDateString("nl-NL").replace(/\//g, "-");

    const response = await fetch(`/api/get/voltage/day/${day}`);
    const data = await response.json();

    // Backend returns an array of objects to merge them
    const merged = Object.assign({}, ...data);

    // Convert it into arrays
    const xLable = Object.keys(merged);        // ["00:00", "01:00", ...]
    const values = Object.values(merged);       // [308.0, 300.0, ...]
    const ctx = document.getElementById("VoltDayChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: xLable,
            datasets: [
                {
                    label: "Total Voltage",
                    data: values,
                    borderColor: "limegreen",
                    fill: true
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                y: {

                    grid: { color: "white" },
                    ticks: { color: "white", beginAtZero: true }
                },
                x: {
                    grid: { color: "white" },
                    ticks: { color: "white", beginAtZero: true },
                },
            },
        },
    });
}
document.addEventListener("DOMContentLoaded", loadVoltageDay);

//voltage per week chart
async function loadVoltageWeekData() {
    const today = new Date();
    const day = today.toLocaleDateString("nl-NL").replace(/\//g, "-");

    const response = await fetch(`/api/get/voltage/week/${day}`);
    const data = await response.json();

    // Backend returns an array of objects to merge them
    const merged = Object.assign({}, ...data);

    // Convert it into arrays
    const xLable = Object.keys(merged);        // ["26/01/2026", "27/01/2026", ...]
    const values = Object.values(merged);       // [308.0, 300.0, ...]

    const ctx = document.getElementById("VoltWeekChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: xLable,
            datasets: [
                {
                    label: "Total Voltage",
                    data: values,
                    borderColor: "limegreen",
                    fill: true
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                y: {
                    grid: { color: "white" },
                    ticks: { color: "white", beginAtZero: true },
                },
                x: {
                    grid: { color: "white" },
                    ticks: { color: "white", beginAtZero: true },
                },
            },
        },
    });
}
document.addEventListener("DOMContentLoaded", loadVoltageWeekData);

//voltage per month graph
async function loadVoltageMonthData() {
    const today = new Date();
    const day = today.toLocaleDateString("nl-NL").replace(/\//g, "-");

    const response = await fetch(`/api/get/voltage/year/${day}`);
    const data = await response.json();

    // Backend returns an array of objects to merge them
    const merged = Object.assign({}, ...data);

    // Convert it into arrays
    const xLable = Object.keys(merged);        // ["01-01", "02-01", ...]
    const values = Object.values(merged);       // [308.0, 300.0, ...]
    const ctx = document.getElementById("VoltMonthChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: xLable,
            datasets: [
                {
                    label: "Total Voltage",
                    data: values,
                    borderColor: "limegreen",
                    fill: true
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            },
            scales: {
                y: {
                    grid: { color: "white" },
                    ticks: { color: "white", beginAtZero: true },
                },
                x: {
                    grid: { color: "white" },
                    ticks: { color: "white", beginAtZero: true },
                },
            },
        },
    });
}
document.addEventListener("DOMContentLoaded", loadVoltageMonthData);
