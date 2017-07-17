import React, { Component } from 'react';
import Chart from '../Chart';
import Selector from './Selector';
import Data from './Data';
import renderChart from './renderChart'

class CourseSelector extends Component {
  constructor(props) {
    super(props);
    this.data = new Data();
    const selectedCourse = '16ws-01188'//this.data.getCourses()[0]
    this.state = { selectedCourse }

    this.setSelectedCourse = this.setSelectedCourse.bind(this);

  }
  setSelectedCourse(value) {
    this.setState({
      selectedCourse:value
    });
  }
  render() {
    return (
      <div>
        <Selector label="Select a Course"
                  items={this.data.getCourses()}
                  onChange={this.setSelectedCourse}
                  current={this.state.selectedCourse}
                  makeLabel={course => this.data.getTitle(course)}/>
        <div style={{height:'100px'}}/>
        <Chart data={this.data.getDataForCourse(this.state.selectedCourse)} renderChart={renderChart}/>
      </div>);
  }
}

export default CourseSelector;
