import React, { PureComponent } from 'react';
import { FormGroup, FormControl, ControlLabel} from 'react-bootstrap'

class Selector extends PureComponent {
  onChange = event => {
    this.props.onChange(event.target.value);
  }

  render() {
    return (
      <FormGroup>
        <ControlLabel>{this.props.label}</ControlLabel>
        <FormControl componentClass="select"  onChange={this.onChange} value={this.props.current}>
          {this.props.items.map((thing, i) => <option key={i}>{thing}</option>)}
        </FormControl>
      </FormGroup>
    );
  }
}

export default Selector;
