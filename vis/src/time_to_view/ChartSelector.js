import React, { Component } from 'react';
import Chart from '../Chart';
import Selector from './Selector';
import Data from './Data';
import renderChart from './renderChart'

class ChartSelector extends Component {
  constructor(props) {
    super(props);
    this.data = new Data();
    const selectedCourse = '16ws-03888'//this.data.getCourses()[0]
    const selectableDocuments = this.data.getDocumentsForCourse(selectedCourse)
    this.state = { 
      selectedCourse,
      selectableDocuments,
      selectedDocument: selectableDocuments[0]
    };

    this.setSelectedDocument = this.setSelectedDocument.bind(this);
    this.setSelectedCourse = this.setSelectedCourse.bind(this);

  }
  setSelectedCourse(value) {
    const selectedCourse = value
    const selectableDocuments = this.data.getDocumentsForCourse(selectedCourse)
    this.setState({
      selectedCourse,
      selectableDocuments,
      selectedDocument: selectableDocuments[0]
    });
  }
  setSelectedDocument(value) {
    this.setState({selectedDocument: value});
  }
  render() {
    return (
      <div>
        <Selector items={this.data.getCourses()} onChange={this.setSelectedCourse} current={this.state.selectedCourse}/>
        <Selector items={this.state.selectableDocuments} onChange={this.setSelectedDocument} current={this.state.selectedDocument}/>
        <Chart data={this.data.getDataForDocument(this.state.selectedCourse,this.state.selectedDocument)} renderChart={renderChart}/>
      </div>);
  }
}

export default ChartSelector;
