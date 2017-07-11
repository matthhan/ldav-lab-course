import React, { Component } from 'react';
import CourseSelector from './CourseSelector';
import { Col, Panel} from 'react-bootstrap'

class TimeSpent extends Component {
  render() {
    return (
      <Col xs={10} sm={10} md={10} lg={10} xsOffset={1} smOffset={1} mdOffset={1} lgOffset={1} style={{marginTop:'20px'}}>
        <Panel>
          <h2> Time Spent On Activities</h2>
          <CourseSelector/>
        </Panel>
      </Col>
    );
  }
}

export default TimeSpent;
