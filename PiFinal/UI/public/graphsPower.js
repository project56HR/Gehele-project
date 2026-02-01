
// power per day graph
async function loadPowerDayData() {

    const today = new Date();
    const day = today.toLocaleDateString("nl-NL").replace(/\//g, "-");

    const response = await fetch(`/api/get/watt/day/${day}`);
    const data = await response.json();

    // Backend returns an array of objects to merge them
    const merged = Object.assign({}, ...data);

    // Convert it into arrays
    const xLable = Object.keys(merged);        
    const values = Object.values(merged);       // [308.0, 300.0, ...]
    const ctx = document.getElementById("PowerDayChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: xLable,
            datasets: [
                {
                    label: "Total Power Usage",
                    data: values,
                    borderColor: "limegreen",
                    fill: true
                }
            ]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: "white" }, ticks: { color: "white", beginAtZero: true } },
                x: { grid: { color: "white" }, ticks: { color: "white" } }
            },
        },
    });
}
document.addEventListener("DOMContentLoaded", loadPowerDayData);

//power per week graph
async function loadPowerWeekData() {
    // Dutch date format (DD-MM-YYYY) 
    const today = new Date(); 
    const day = today.toLocaleDateString("nl-NL").replace(/\//g, "-");
    
    const response = await fetch(`/api/get/watt/week/${day}`);
    const data = await response.json();

    // Backend returns an array of objects to merge them
    const merged = Object.assign({}, ...data);

    // Convert it into arrays
    const xLable = Object.keys(merged);        
    const values = Object.values(merged);       // [308.0, 300.0, ...]

    const ctx = document.getElementById("PowerWeekChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: xLable,
            datasets: [{
                label: "Weekly Power Usage",
                data: values,
                borderColor: "limegreen",
                fill: true
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: "white" }, ticks: { color: "white", beginAtZero: true } },
                x: { grid: { color: "white" }, ticks: { color: "white" } }
            }
        }
    });
}
document.addEventListener("DOMContentLoaded", loadPowerWeekData);

//Power per month graph
async function loadPowerMonthData() {
    // Dutch date format (DD-MM-YYYY) 
    const today = new Date(); 
    const day = today.toLocaleDateString("nl-NL").replace(/\//g, "-"); 
    
    const response = await fetch(`/api/get/watt/year/${day}`); 
    const data = await response.json(); 
    
    // Backend returns an array of objects to merge them
    const merged = Object.assign({}, ...data);

    // Convert it into arrays
    const xLable = Object.keys(merged);        
    const values = Object.values(merged);      
    
    const ctx = document.getElementById("PowerMonthChart").getContext("2d");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: xLable,
            datasets: [{
                label: "Monthly Power Usage",
                data: values,
                borderColor: "limegreen",
                fill: true
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                y: { grid: { color: "white" }, ticks: { color: "white", beginAtZero: true } },
                x: { grid: { color: "white" }, ticks: { color: "white" } }
            }
        }
    });
}
document.addEventListener("DOMContentLoaded", loadPowerMonthData);
