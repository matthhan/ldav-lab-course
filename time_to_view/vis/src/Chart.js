
import React, { PureComponent } from 'react';

class Chart extends PureComponent {
  render() {
    return (<div>chart goes here {JSON.stringify(this.props.data)}</div>);
  }
}

export default Chart;
