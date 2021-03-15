import React, { Component } from 'react';
import BalanceWS from './tools/balance'
import Chart from './tools/chart'

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
        <Chart onChange={this.eventhandler}/>
        <div>
          <p>Account Balance: </p>
        </div>
        <BalanceWS/>
      </div>
    );
  }
}

export default App;