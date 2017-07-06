import React, { PureComponent } from 'react';

class Selector extends PureComponent {
  render() {
    return (
      <select onChange={this.props.onChange} value={this.props.current} selected={this.props.current}>
        {this.props.items.map((thing, i) => <option key={i}>{thing}</option>)}
      </select>
    );
  }
}

export default Selector;
