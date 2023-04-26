// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

const pieChartData = 'static/document/ZoneTotalPlayTime.csv';

d3.csv(pieChartData).then(function(datapoints){
  removePieAllData(myPieChart);
  addPieData(myPieChart,datapoints[0].ZoneT);
  addPieData(myPieChart,datapoints[0].ZoneA);
  addPieData(myPieChart,datapoints[0].ZoneB);
  addPieData(myPieChart,datapoints[0].ZoneC);
  addPieData(myPieChart,datapoints[0].ZoneD);
  addPieData(myPieChart,datapoints[0].ZoneE);
});

function addPieData(chart, data) {
  chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
  });
  chart.update()
}

function removePieData(chart) {
  chart.data.datasets.forEach((dataset) => {
      dataset.data.pop();
  });
  chart.update()
}

function removePieAllData(chart){
  for(var i = 0; i < 6; i++)
  {
    chart.data.datasets.forEach((dataset) => {
      dataset.data.pop();
    });
  }
  myLineChart.update();
}

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Zone T', 'Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E'],
    datasets: [{
      data: [],
      backgroundColor: ['#454545','#00A8C6', '#40C0CB', '#F9F2E7' , '#AEE239','#8FBE00'],
      hoverBackgroundColor: ['#1c1c1c','#029ab5', '#3aabb5', '#e8e1d5' , '#a1d134','#83ad00'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
