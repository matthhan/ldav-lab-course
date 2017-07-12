import React, { Component } from 'react';
import VirtualizedSelect from 'react-virtualized-select';

import 'react-select/dist/react-select.css'
class Selector extends Component {
  render() {
    return (
        <VirtualizedSelect 
          autofocus 
          searchable
          clearable={false}
          multi={false}
          onChange={this.props.onChange}
          simpleValue
          value={this.props.current}
          options={this.props.items.map(x => {return {label:x,value:x}})}/>
    );
  }
}

export default Selector;
