import React, { Component } from 'react';
import ChartSelector from './ChartSelector';
import { Panel, Col} from 'react-bootstrap'

class TimeToView extends Component {
  render() {
    return (
      <Col xs={10} sm={10} md={10} lg={10} xsOffset={1} smOffset={1} mdOffset={1} lgOffset={1} style={{marginTop:'20px'}}>
        <Panel>
            <h2> Time until Seen</h2>
            <ChartSelector/>
        </Panel>
      </Col>
    );
  }
}

export default TimeToView;
