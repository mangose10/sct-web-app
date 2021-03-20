import React, { Component } from 'react'
import Canvas from './canvas'
import './../css/chart.css'
//import { connect } from 'react-redux'

class KlineWs extends Component {
  
  state = {
    ws: null,
    curObj: {},
    histData: {},
    margin: {},
    interval: '1m'
  };

  getMLines = async () => {
    const response = await fetch('/api/get-margin-lines')
    const body = await response.text();
    let temp = body.replaceAll("'", "\"").replace("\r", "").replace("\n", "");
    //console.log(temp)
    this.setState({margin: JSON.parse(temp)});
  }

  getBalance = () => {
    let temp = this.state.margin
    if (Object.keys(temp).length < 2){
      return 0;
    }else if (Object.keys(temp).length > 4){
      return temp.sell.price * temp.BTCbought;
    }else if (Object.keys(this.state.curObj).length){
      return this.state.curObj.c * temp.BTCbought;
    }
  }
  
  // single websocket instance for the own application and constantly trying to reconnect.

  componentDidMount() {
    this.connect();    
  }
  componentDidUpdate(){
    if (this.state.interval !== this.props.interval){
        this.state.ws.close();
        this.setState({interval:this.props.interval})
        this.setState({histData:{}})
        this.connect();
    }
  }

  timeout = 250; // Initial timeout duration as a class variable

  /**
   * @function connect
   * This function establishes the connect with the websocket and also ensures constant reconnection if connection closes
   */
  connect = () => {
      var ws = new WebSocket("wss://stream.binance.us:9443/ws/btcusd@kline_"+this.props.interval);
      let that = this; // cache the this
      var connectInterval;

      // websocket onopen event listener
      ws.onopen = () => {
          console.log("connected websocket main component");

          this.setState({ ws: ws });

          that.timeout = 250; // reset timer to 250 on open of websocket connection 
          clearTimeout(connectInterval); // clear Interval on on open of websocket connection
      };

      // websocket onclose event listener
      ws.onclose = e => {
          console.log(
              `Socket is closed. Reconnect will be attempted in ${Math.min(
                  10000 / 1000,
                  (that.timeout + that.timeout) / 1000
              )} second.`,
              e.reason
          );

          that.timeout = that.timeout + that.timeout; //increment retry interval
          connectInterval = setTimeout(this.check, Math.min(10000, that.timeout)); //call check function after timeout
      };

      ws.onmessage = msg => {
        
        this.getMLines();

        //console.log("here")
        //console.log(this.props.data)
        if (!Object.keys(this.state.histData).length && (this.props.data.length > 1)){
            
            this.setState({histData:JSON.parse(this.props.data)})
            this.setState({interval:this.props.interval})
            //console.log(this.state.histData)
        }else if (!Object.keys(this.state.histData).length) {return}

        let obk = JSON.parse(msg.data).k
        obk = {
          'T':obk['T'],
          'c':obk['c'].slice(0, -4),
          'h':obk['h'].slice(0, -4),
          'l':obk['l'].slice(0, -4),
          'o':obk['o'].slice(0, -4),
          't':obk['t']
        }

        //console.log(this.state.curObj)
        if (!Object.keys(this.state.curObj).length){
          this.setState({curObj:obk});
          console.log("was empty")
          return;
        }

        if (Object.keys(obk).length && obk.t > this.state.curObj.T){
            let temp = this.state.histData;
            temp.klinedata.shift();
            temp.klinedata.push(this.state.curObj)
            temp.max = temp.max < obk.h ? obk.h : temp.max;
            temp.min = temp.min > obk.l ? obk.l : temp.min;
            this.histData = temp
        }
        this.setState({curObj:obk})
      };

      // websocket onerror event listener
      ws.onerror = err => {
          console.error(
              "Socket encountered error: ",
              err.message,
              "Closing socket"
          );

          ws.close();
      };
  };

  /**
   * utilited by the @function connect to check if the connection is close, if so attempts to reconnect
   */
  check = () => {
      const { ws } = this.state;
      if (!ws || ws.readyState === WebSocket.CLOSED) this.connect(); //check if websocket instance is closed, if so call `connect` function.
  };

  render() {
      return (
        <div>
          <div class="chartContainer">
              <Canvas width="900" height="500" data={this.state.histData} cur={this.state.curObj} margin={this.state.margin} class="chart"/>
          </div>
          <p>Balance: {"\n"+this.getBalance()}</p>
        </div>
      );
  }
}

export default KlineWs