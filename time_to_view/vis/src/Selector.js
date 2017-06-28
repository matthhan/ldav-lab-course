import React, { PureComponent } from 'react';

class Selector extends PureComponent {
  valuesToShow = () => 
    this.props.items
      .map(decodeURIComponent)
      .map(x => x.replace(/ +/g,' '));
  originalValueOf = showValue => 
    this.props.items[this.valuesToShow().findIndex(thing => thing.normalize() === showValue.normalize())];
  onChange = event => {
    this.props.onChange(this.originalValueOf(event.target.value));
  }

  render() {
    return (
      <select onChange={this.onChange} selected={this.props.current}>
        {this.valuesToShow().map((thing, i) => <option key={i}>{thing}</option>)}
      </select>
    );
  }
}

export default Selector;
