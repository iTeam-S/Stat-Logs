var xValues = [...Array(24).keys()];
          
new Chart("myChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{ 
      data: {{ liste1 }},
      borderColor: "red",
      fill: false
    }]
  },
  options: {
    legend: {display: false}
  }
})