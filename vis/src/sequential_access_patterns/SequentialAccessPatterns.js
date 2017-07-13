import React, { Component } from 'react'
import data from './data.json';
import Chart from '../Chart'
import renderChart from './renderChart'
import { Panel, Col } from 'react-bootstrap'
import MathJax from 'react-mathjax'


export default class SequentialAccessPatterns extends Component {
  render() {
    return (
      <Col xs={10} sm={10} md={10} lg={10} xsOffset={1} smOffset={1} mdOffset={1} lgOffset={1} style={{marginTop:'20px'}}>
        <Panel>
      <h1>Sequential Access Patterns Sorted by Badness</h1>
      <MathJax.Context><MathJax.Node inline>{`\\text{Badness} = \\log_{10}(\\text{#Occurences}^{\\text{Pattern Length}})`}</MathJax.Node></MathJax.Context>
      <Chart data={data} renderChart={renderChart}/>
        </Panel>
      </Col>
      )
  }
}
