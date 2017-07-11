import React, { PureComponent } from 'react';
import { FormControl, FormGroup, ControlLabel } from 'react-bootstrap';

class Selector extends PureComponent {
  render() {
    return (
      <FormGroup>
        <ControlLabel>{this.props.label}</ControlLabel>
        <FormControl componentClass="select" onChange={this.props.onChange} value={this.props.current} selected={this.props.current}>
          {this.props.items.map((thing, i) => <option key={i}>{thing}</option>)}
        </FormControl>
      </FormGroup>
    );
  }
}

export default Selector;
