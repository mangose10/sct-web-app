import React, { Component } from 'react';
import KlineWs from './tools/kline-ws'
import Chart from './tools/chart'

class App extends Component {
  state = {
    response: '',
    post: '',
    responseToPost: '',
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