import Highcharts from 'highcharts';

const getPercentageVisited = (data) => {
  const numbers = data.accesses.map((x,i) => i);
  return numbers.map(x => (x+1) / numbers.length);
}
const sorted = (arr) => {
  const newarr = arr.map(x => x);
  newarr.sort((x,y) => x - y);
  return newarr;
}
const getTimes = (data) => sorted(data.accesses);
const getPlotArr = (data) => getTimes(data).map((time,i) => [time,getPercentageVisited(data)[i]]);

export default function renderChart(data,chartcontainer) {
  Highcharts.chart('chartcontainer', {
    chart: {
      type: 'line'
    },
    xAxis: {
      ordinal:false,
    },
    series: [{data: getPlotArr()}]
  });
}
