import React, { useRef, useEffect } from 'react'
import mousePosition from 'mouse-position'

const Canvas = props => {

  const canvasRef = useRef(null)
  
  var obj
  var max
  var min
  var offset
  var flatOff
  var lineWidth
  var center

  const hover = ctx => {
    let mouse = mousePosition(canvasRef.current)
    let x = parseInt(mouse['0']/lineWidth)*lineWidth + center

    console.log(mouse.prev['0'])
    ctx.beginPath()
    ctx.moveTo(x, 0)
    ctx.lineTo(x, canvasRef.current.width)
    ctx.stroke()
    ctx.closePath()
  }

  const drawline = ctx => {

    
    try {
      obj = props.data
      max = obj.max;
      min = obj.min;
      offset = ((max-min)/canvasRef.current.height)/0.7;
      flatOff = (canvasRef.current.height - (max-min)/offset)/2;

      obj = obj.klinedata;
      lineWidth = Math.floor(canvasRef.current.width/120)
      center = (lineWidth/2)
      let red = "#e50000"
      let green = "#009d00"
      
      var i = 0
      for(i; i < obj.length; i++){
        let color = parseFloat(obj[i]['o']) > parseFloat(obj[i]['c']) ? red : green;
        let start = parseFloat(obj[i]['o']) > parseFloat(obj[i]['c']) ? 'o' : 'c';

        ctx.beginPath()
        ctx.moveTo((i*lineWidth)+center, Math.floor(flatOff+(max-(parseFloat(obj[i]['h'])))/offset))
        ctx.lineTo((i*lineWidth)+center, Math.floor(flatOff+(max-(parseFloat(obj[i]['l'])))/offset))
        ctx.strokeStyle = color
        ctx.stroke()
        ctx.closePath()

        ctx.fillStyle = color
        ctx.strokeStyle = "#000"
        
        ctx.rect(i*lineWidth, Math.floor(flatOff+(max-(parseFloat(obj[i][start])))/offset), lineWidth, Math.floor(Math.abs(parseFloat(obj[i]['o'])-parseFloat(obj[i]['c']))/offset));
        ctx.stroke()
        ctx.fill()
      }
      let color = parseFloat(obj[i]['o']) > parseFloat(obj[i]['c']) ? red : green;
      let start = parseFloat(obj[i]['o']) > parseFloat(obj[i]['c']) ? 'o' : 'c';
      ctx.fillStyle = color
      ctx.fillRect(i*lineWidth, Math.floor(flatOff+(max-(parseFloat(props.cur[start])))/offset), lineWidth, Math.floor(Math.abs(parseFloat(props.cur['o'])-parseFloat(props.cur['c']))/offset));
      ctx.beginPath()
      ctx.moveTo((i*lineWidth)+center, Math.floor(flatOff+(max-(parseFloat(props.cur['h'])))/offset))
      ctx.lineTo((i*lineWidth)+center, Math.floor(flatOff+(max-(parseFloat(props.cur['l'])))/offset))
      ctx.strokeStyle = color
      ctx.stroke()
      ctx.closePath()

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
    ctx.strokeStyle = '#fff';
    ctx.fillStyle = "#fff";
    let buyHeight = Math.floor(flatOff+(max-props.margin.buy.price)/offset);
    ctx.moveTo(0, buyHeight);
    ctx.lineTo(canvasRef.current.width-1, buyHeight);
    
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
    hover(context)
  }, [drawMargin, drawline, hover])
  
  return <canvas ref={canvasRef} {...props}/>
}

export default Canvas