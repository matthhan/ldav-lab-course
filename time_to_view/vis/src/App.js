import React, { Component } from 'react';
import './App.css';
import ChartSelector from './ChartSelector';

class App extends Component {
  render() {
    return (
      <div className="App">
        <h2> Time until Seen</h2>
        <ChartSelector/>
      </div>
    );
  }
}

export default App;
