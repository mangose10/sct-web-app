import React, { useRef, useEffect } from 'react'

const Canvas = props => {

  const canvasRef = useRef(null)
  
  var obj
  var max
  var min
  var offset
  var flatOff

  const drawline = ctx => {

    
    try {
      obj = props.data
      max = obj.max;
      min = obj.min;
      offset = ((max-min)/canvasRef.current.height)/0.7;
      flatOff = (canvasRef.current.height - (max-min)/offset)/2;

      obj = obj.klinedata;

      ctx.beginPath()
      ctx.moveTo(0, Math.floor(flatOff+(max-(parseFloat(obj[0]['c'])))/offset));
    
      var i = 1
      for(i; i < obj.length; i++){
        ctx.lineTo(i*3, Math.floor(flatOff+(max-(parseFloat(obj[i]['c'])))/offset));
      }
      ctx.lineTo(i*3, Math.floor(flatOff+(max-(parseFloat(props.cur['c'])))/offset));

      ctx.strokeStyle = '#e8b923'
      ctx.stroke();
      ctx.closePath()
    } catch (error) {
      //console.error(error);
    }
    
  }

  const drawMargin = ctx => {

    ctx.clearRect(0,0,500,1000);
    ctx.fillStyle = "#333";
    ctx.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height); 
    
    //console.log(props.margin.length())
    if (Object.keys(props.margin).length < 2){
      return;
    }
    ctx.beginPath();

    let buyHeight = Math.floor(flatOff+(max-props.margin.buy.price)/offset);
    ctx.moveTo(0, buyHeight);
    ctx.lineTo(canvasRef.current.width-1, buyHeight);
    
    ctx.strokeStyle = '#fff';
    ctx.fillStyle = "#fff";
    ctx.stroke();
    ctx.closePath();

    ctx.font = '12px serif';
    ctx.fillStyle = "#fff";
    ctx.fillText('Buy price: ' + (props.margin.buy.price), 10, 20);

    ctx.beginPath();
    let sellPrice = props.margin.break/props.margin.BTCbought;
    let sellHeight = Math.floor(flatOff+(max-sellPrice)/offset);

    ctx.moveTo(0, sellHeight);
    ctx.lineTo(canvasRef.current.width, sellHeight);

    ctx.strokeStyle = "#fff";
    ctx.fillStyle = "#fff";
    ctx.stroke();
    ctx.closePath();

    let accountVal = props.cur.c*props.margin.BTCbought;

    

    //sendToApp({'accountVal':accountVal})
    console.log(accountVal);
  }

  useEffect(() => {
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')
    
    drawMargin(context)
    drawline(context)
  }, [drawMargin, drawline])
  
  return <canvas ref={canvasRef} {...props}/>
}

export default Canvas