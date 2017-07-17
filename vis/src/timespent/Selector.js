import React, { Component } from 'react';

import 'react-select/dist/react-select.css'
import 'react-virtualized/styles.css'
import 'react-virtualized-select/styles.css'
import VirtualizedSelect from 'react-virtualized-select';

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
          options={this.props.items.map(x => {return {label:this.props.makeLabel(x),value:x}})}/>
    );
  }
}

export default Selector;
