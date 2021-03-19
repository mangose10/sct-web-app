import React, { Component } from 'react';
import Chart from './tools/chart'
import CalendarWrapper from './tools/calendar'

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
        <CalendarWrapper/>
      </div>
    );
  }
}

export default App;