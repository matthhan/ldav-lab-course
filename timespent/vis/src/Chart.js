import React, { PureComponent } from 'react';
import renderChart from './renderChart.js';

class Chart extends PureComponent {
  
  componentDidMount() {
    this.componentDidUpdate();
  }
  componentDidUpdate() {
    renderChart(this.props.data,'chartcontainer')
  }
  render() {
    return (<div id="chartcontainer"/>);
  }
}

export default Chart;
