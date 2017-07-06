import React, { Component } from 'react';
import ChartSelector from './ChartSelector';

class TimeToView extends Component {
  render() {
    return (
      <div className="App">
        <h2> Time until Seen</h2>
        <ChartSelector/>
      </div>
    );
  }
}

export default TimeToView;
