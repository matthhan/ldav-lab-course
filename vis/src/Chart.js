import React, { Component } from 'react'
class Chart extends Component {
  componentDidMount() {
    this.componentDidUpdate();
  }
  componentDidUpdate() {
    this.props.renderChart(this.props.data,'chartcontainer')
  }
  render() {
    return (<div id="chartcontainer"/>);
  }
}

export default Chart;
