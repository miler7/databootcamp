function buildMetadata(sample) {

  // Use `d3.json` to fetch the metadata for a sample
    var metaurl = `/metadata/${sample}`;
    d3.json(metaurl).then(function(sample){

    // Use d3 to select the panel with id of `#sample-metadata`
      var sample_metadata = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
      sample_metadata.html("");

    // Use `Object.entries` to add each key and value pair to the panel
      Object.entries(sample).forEach(function ([key, value]) {
        var row = sample_metadata.append("p");
        row.text(`${key}: ${value}`);
      });
    })
};

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  var charturl = `/samples/${sample}`;
  d3.json(charturl).then(function(sample){

    // @TODO: Build a Bubble Chart using the sample data
    var trace1 = {
      x: sample.otu_ids,
      y: sample.sample_values,
      text: sample.otu_labels,
      mode: 'markers',
      marker: {
        color: sample.otu_ids,
        size: sample.sample_values
      } 
    };

    var bubbledata = [trace1];

    var layout = {
      xaxis: {title: "OTU ID"},
    };

    Plotly.newPlot("bubble", bubbledata, layout);

    // @TODO: Build a Pie Chart
    var trace2 = {
      values: sample.sample_values.slice(0,10),
      labels: sample.otu_ids.slice(0,10),
      hovertext: sample.otu_labels.slice(0,10),
      type: 'pie'
    };

    var piedata = [trace2];

    var layout = {};

    Plotly.newPlot("pie", piedata, layout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
