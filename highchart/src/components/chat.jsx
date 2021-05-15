import React, { useEffect, useState } from "react";
import HighchartsReact from "highcharts-react-official";
// Import Highcharts
import Highcharts from "highcharts/highcharts.src.js";
import LabelComponent from "./label";
import { useSelector } from "react-redux";

export default function Chart(props) {
  const [internalChart, setInterChart] = useState(null);
  const { data } = useSelector(
    (state) => state.commonProps
  );
  console.log(data)
  let chartOptions = {
    series: [
      {
        data: data[1]
      }
    ],
    xAxis: {
      categories: data,
      labels: {
        useHTML: true,
        formatter: function () {
          return "";
        }
      }
    }
  }



  function afterChartCreated(chart) {
    setInterChart(chart)
  }

  useEffect(() => {
    if (internalChart) {
      console.log("here")
      internalChart.reflow();
    }
  })
  const chart = internalChart,
    customLabels = [];

  if (chart && chart.xAxis[0]) {
    Highcharts.objectEach(chart.xAxis[0].ticks, function (tick) {
      customLabels.push(<LabelComponent tick={tick} />);
    });
  }
  return (
    <div>
      <HighchartsReact
        highcharts={Highcharts}
        options={chartOptions}
        callback={afterChartCreated}
      />
      {customLabels}
    </div>
  );

}
