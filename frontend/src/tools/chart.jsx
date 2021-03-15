//import mongoose from "mongoose";
import React, { Component } from 'react'
import KlineWs from './kline-ws';

class Chart extends Component {

  

  constructor(props){
    super(props)
    this.state = {
      post: '1m',
      klineData: '',
    };
    this.getDataPoints = this.getDataPoints.bind(this);
  }

  componentDidMount(){
    this.getDataPoints();
  }

  getDataPoints = async () => {
    const response = await fetch('/api/get-kline-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ post: this.state.post }),
    });
    const body = await response.text();
    
    this.setState({ klineData: body });
  };

  
  
  componentDidUpdate(){
    //this.getDataPoints();
  }
  
  render() {
    return(
      <div>
        
        <select 
          value={this.state.post}
          onChange={async e => {
            this.setState({ post: e.target.value });
            this.getDataPoints();
          }}
        >
          <option value="1m">1m</option>
          <option value="5m">5m</option>
          <option value="30m">30m</option>
          <option value="1h">1h</option>
        </select>
        <KlineWs data={this.state.klineData} interval={this.state.post} onChange={this.props.onChange}/>
      </div>
  )};
}

export default Chart;
