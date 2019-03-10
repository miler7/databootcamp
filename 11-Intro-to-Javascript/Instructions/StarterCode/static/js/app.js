// from data.js
var tableData = data;

// Reference the table body
var tbody = d3.select("tbody");

// Populate table with data
tableData.forEach((UFOsighting) => {
    var row = tbody.append("tr");

    Object.entries(UFOsighting).forEach(([key,value]) => {
        var cell = tbody.append("td");
        cell.text(value);
    });
})