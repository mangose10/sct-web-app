import React, { Component } from "react";

class Transaction extends Component {
  state = {
    listitems: this.props.trans
  };

  componentDidUpdate(){
    
  }

  render() {
    return (
      <React.Fragment>
        <ul className="list-group">
          {this.props.trans.map(trans => (
            <li>
              {trans.BTCbought}
            </li>
          ))}
        </ul>
      </React.Fragment>
    );
  }
}

export default Transaction;