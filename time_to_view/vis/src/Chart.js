
import React, { PureComponent } from 'react';
import Highcharts from 'highcharts';

class Chart extends PureComponent {
  getPercentageVisited() {
    const numbers = this.props.data.accesses.map((x,i) => i)
    return numbers.map(x => (x+1) / numbers.length)
  }
  getTimes() {
    return this.sorted(this.props.data.accesses);
  }
  getPlotArr() {
    return this.getTimes().map((time,i) => [time,this.getPercentageVisited()[i]]);
  }
  sorted(arr) {
    const newarr = arr.map(x => x);
    newarr.sort((x,y) => x - y);
    return newarr;
  }
  
  componentDidMount() {
    this.componentDidUpdate();
  }
  componentDidUpdate() {
    Highcharts.chart('chartcontainer', {
      chart: {
        type: 'line'
      },
      xAxis: {
        ordinal:false,
      },
      series: [{data: this.getPlotArr()}]
    });
  }
  render() {
    return (<div id="chartcontainer"/>);
  }
}

export default Chart;
