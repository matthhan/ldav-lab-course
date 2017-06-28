import React, { Component } from 'react';
import Chart from './Chart';
import Selector from './Selector';
import Data from './Data';

class CourseSelector extends Component {
  constructor(props) {
    super(props);
    this.data = new Data();
    const selectedCourse = '16ws-01188'//this.data.getCourses()[0]
    this.state = { selectedCourse }

    this.setSelectedCourse = this.setSelectedCourse.bind(this);

  }
  setSelectedCourse(event) {
    this.setState({
      selectedCourse:event.target.value
    });
  }
  render() {
    return (
      <div>
        <Selector items={this.data.getCourses()} onChange={this.setSelectedCourse} current={this.state.selectedCourse}/>
        <div style={{height:'100px'}}/>
        <Chart data={this.data.getDataForCourse(this.state.selectedCourse)}/>
      </div>);
  }
}

export default CourseSelector;
