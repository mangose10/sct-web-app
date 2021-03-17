import React, { Component } from 'react';
import BalanceWS from './tools/balance'
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
        {/*<ThreeDotsWave/>*/}
      </div>
    );
  }
}

export default App;