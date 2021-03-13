import React, { Component } from 'react'
import Canvas from './canvas'
//import { connect } from 'react-redux'

class KlineWs extends Component {
  constructor(props) {
      super(props);

      this.state = {
          ws: null,
          curObj: {},
          histData: {},
          interval: '1m'
      };
  }

  
  // single websocket instance for the own application and constantly trying to reconnect.

  componentDidMount() {
    this.connect();    
  }
  componentDidUpdate(){
    if (this.state.interval != this.props.interval){
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
      var ws = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_"+this.props.interval);
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
          
        if (!Object.keys(this.state.histData).length && (this.props.data.length > 1)){
            this.setState({histData:JSON.parse(this.props.data)})
            this.setState({interval:this.props.interval})
        }else {return}
        //console.log(this.props)

        let obk = JSON.parse(msg.data).k
        if (!Object.keys(this.state.curObj).length || obk.t > this.state.curObj.T){
            let temp = this.state.histData;
            //console.log(temp);
            temp.klinedata.shift();
            temp.klinedata.push(this.state.curObj)
            temp.max = temp.max < obk.h ? obk.h : temp.max;
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
        <div margin="25px">
            <Canvas width="500" height="200" data={this.state.histData} cur={this.state.curObj}/>
        </div>
      );
  }
}

export default KlineWs