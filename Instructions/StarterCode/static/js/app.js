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

// Select the filter button
var filter = d3.select("#filter-btn");

// Complete the click handler for the form
filter.on("click", function() {

    // Prevent the page from refreshing
    d3.event.preventDefault();

    // Clear existing table
    d3.selectAll("tbody tr").remove();
    d3.selectAll("tbody td").remove();

    // Select the input element and get the raw HTML node
    var inputElement = d3.select("#datetime");

    // Get the value property of the input element
    var inputValue = inputElement.property("value");

    // Use the form input to filter the data by date
    var filteredData = tableData.filter(sighting => sighting.datetime === inputValue);

    // Reference the table body
    var tbody = d3.select("tbody");

    // Populate table with data
    filteredData.forEach((UFOsighting) => {
        var row = tbody.append("tr");

        Object.entries(UFOsighting).forEach(([key,value]) => {
            var cell = tbody.append("td");
            cell.text(value);
        });
    })

});

