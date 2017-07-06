import React, { Component } from 'react';
import { Nav, NavItem } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.css'
import TimeSpent from './timespent/TimeSpent'
import TimeToView from './time_to_view/TimeToView'
import SequentialAccessPatterns from './sequential_access_patterns/SequentialAccessPatterns';

class App extends Component {
  constructor(props) {
    super(props)

    this.state = {selected:1}
  }
  render() {
    return (
      <div>
        <Nav bsStyle="tabs" activeKey={this.state.selected} onSelect={event =>this.setState({selected:event})}>
          <NavItem eventKey={1}>Sequential Access Patterns</NavItem>
          <NavItem eventKey={2}>Time Spent</NavItem>
          <NavItem eventKey={3}>Time To View</NavItem>
        </Nav>
        <div>
          {(this.state.selected === 1) && <SequentialAccessPatterns/>}
          {(this.state.selected === 2) && <TimeSpent/>}
          {(this.state.selected === 3) && <TimeToView/>}
        </div>
      </div>
    );
  }
}

export default App;
