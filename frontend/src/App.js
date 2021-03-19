import React, { Component } from 'react';
import Chart from './tools/chart'
import ThreeDotsWave from './tools/loading'

class App extends Component {
  state = {
    response: '',
    post: '',
    responseToPost: '',
    chartVals: {}
  };
  
  
  
  render() {
    return (
      <div>
        <Chart/>
      </div>
    );
  }
}

export default App;