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
const getInitialUpload = (data) => data.initial
const getTimes = (data) => sorted(data.accesses);
const getPlotArr = (data) => getTimes(data).map((time,i) => [time,getPercentageVisited(data)[i]]);

function formatSecondsAsDate() {
  return hours(this.value)
}
const hours = seconds => Math.round(seconds / (60*60))
function formatPercent() {
  return percent(this.value)
}
const percent = (x) => Math.round(x * 100) + "%"
function formatTooltip() {
  return `After ${hours(this.x)} hours, ${percent(this.y)} of the students had seen the document.`;
}
export default function renderChart(data,chartcontainer) {
  Highcharts.chart('chartcontainer', {
    chart: {
      type: 'line'
    },
    xAxis: {
      ordinal:false,
      title: {
        text: 'Hours',
      },
      labels: {
        formatter: formatSecondsAsDate
      },
      tickInterval: (60*60),
    },
    yAxis: { 
      max: 1,
      title: {
        text: 'Percent of Students Viewed Document',
      },
      labels: {
        formatter: formatPercent
      },
    },
    series: [{data: getPlotArr(data),showInLegend: false}],
    title: {
      text: `Time Until File was Seen after it was uploaded at ${getInitialUpload(this.data)}`,
    },
    tooltip: {
      formatter: formatTooltip
    }
  });
}
