import React, { useState, useEffect, Component } from 'react'
import './../css/calendar.css'
import $ from 'jquery'
import Calendar from 'react-calendar'
import Transaction from './transactionList'


const CalendarWrapper = props => {

  const [value, onChange] = useState(new Date());
  const [trans, setTrans] = useState([])
  const [prevTime, upTime] = useState(value.getTime())
  //var prevTime = value.getTime();
  const months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  
  function UNIXtoString(time){
    let currentTimestamp = new Date(time)
    console.log(currentTimestamp); // get current timestamp
    let date = new Intl.DateTimeFormat('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(currentTimestamp)
    return date;
  }

  function getTimeSpan(time){

    let timeType = 'ms'
    if (time/1000 > 1){
      time /= 1000;
      timeType = 's'
      if (time/60 > 1){
        time /= 60;
        timeType = 'm'
        if (time/60 > 1){
          time /= 60;
          timeType = 'h'
          if (time/24 > 1){
            time /= 24;
            timeType = 'd'
            if (time/7 > 1){
              time /= 7;
              timeType = 'w'
            }
          }
        }
      }
    }
    return ""+time+timeType
  }

  async function getTrans() {
    const response = await fetch('/api/get-trans-by-date', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ post: value.getTime() }),
    });
    const body = await response.text();
    if (body.length > 10){
      //console.log(body)
      let parsed = JSON.parse(body)
      if (Object.keys(parsed[parsed.length-1]).length < 1){

      }else if (Object.keys(parsed[parsed.length-1]).length < 4){
        parsed.splice(parsed.length-1, parsed.length)
      }
      let totals = {'pChange':1, dChange:0};
      for (let i = 0; i < parsed.length; i++){
        parsed[i].buy.time = UNIXtoString(parsed[i].buy.time)
        parsed[i].change.timeSpan = getTimeSpan(parsed[i].change.timeSpan)
        totals.pChange *= 1+parsed[i].change.percent
        totals.pChange += parsed[i].change.percent*parsed[i].buy.price*parsed[i].BTCbought
      }
      parsed[0].totalChange = totals
      updateTrans(parsed)
    }else{
      updateTrans([])
    }
  };

  function updateTrans(val){
    setTrans(val)
  }
  
  useEffect(() =>{
    if (prevTime != value.getTime()){
      getTrans()
      upTime(value.getTime())
    }
  }, [getTrans])

  return (
    <div display="inline-block">
      <div class="calendar-wrapper">
        <Calendar
          onChange={onChange}
          value={value}
        />
      </div>
      <div class="transaction-container">
        <p>{months[value.getMonth()]} {value.getDate()}, {value.getFullYear()}</p>
        <table class="trans-table">
          <tr class="trans-header">
            <th>Buy Time</th>
            <th>Duration</th>
            <th>% Change</th>
            <th>$ Change</th>
          </tr>
          {trans.map(trans => (  
            <tr class="trans-info" key={trans.sell.time} 
            onMouseEnter={e=>{$(e.target.parentNode).children('td').css('background-color','#999');}} 
            onMouseLeave={e=>{$(e.target.parentNode).children('td').css('background-color','');}}
            >
              <React.Fragment key={trans.sell.time}>
                <td>{trans.buy.time}</td>
                <td>{trans.change.timeSpan}</td>
                <td>{(trans.change.percent*100).toFixed(4)}%</td>
                <td>${(trans.change.percent*trans.buy.price*trans.BTCbought).toFixed(3)}</td>
              </React.Fragment>
            </tr>
          ))}
          {/*<tr>
            <td>Total</td>
            <td>{getTimeSpan(Date.now()-value.getTime())}</td>
            <td>{(trans[0].change.totalChange.pChange*100).toFixed(4)}%</td>
            <td>${(trans[0].change.totalChange.dChange).toFixed(3)}</td>
          </tr>*/}
        </table>
      </div>
    </div>
  )
}

export default CalendarWrapper;