import React, { Component } from 'react';
import './App.css';
import CourseSelector from './CourseSelector';

class App extends Component {
  render() {
    return (
      <div className="App">
        <h2> Time Spent On Activities</h2>
        <CourseSelector/>
      </div>
    );
  }
}

export default App;
