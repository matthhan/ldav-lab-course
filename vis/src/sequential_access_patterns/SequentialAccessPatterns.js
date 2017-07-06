import React, { Component } from 'react'
import data from './data.json';
import Chart from '../Chart'
import renderChart from './renderChart'


export default class SequentialAccessPatterns extends Component {
  render() {
    return (<Chart data={data} renderChart={renderChart}/>)
  }
}