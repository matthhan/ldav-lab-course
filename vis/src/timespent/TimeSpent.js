import React, { Component } from 'react';
import CourseSelector from './CourseSelector';

class TimeSpent extends Component {
  render() {
    return (
      <div className="App">
        <h2> Time Spent On Activities</h2>
        <CourseSelector/>
      </div>
    );
  }
}

export default TimeSpent;
