import React, { useRef, useEffect } from 'react'

const Canvas = props => {
  
  const canvasRef = useRef(null)
  
  const drawline = ctx => {

    ctx.clearRect(0,0,500,1000);

    ctx.fillStyle = "#333";
    ctx.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height);  
    
    
    try {
      let obj = props.data
      let max = obj.max;
      let min = obj.min;
      let offset = ((max-min)/canvasRef.current.height)/0.7;
      let flatOff = (canvasRef.current.height - (max-min)/offset)/2;

      obj = obj.klinedata;

      ctx.beginPath()
      ctx.moveTo(0, Math.floor(flatOff+(max-(parseFloat(obj[0]['c'])))/offset));
    
      var i = 1
      for(i; i < obj.length; i++){

        //console.log(Math.floor((max-(parseFloat(obj[i]['cPrice'])))/offset));
        ctx.lineTo(i*3, Math.floor(flatOff+(max-(parseFloat(obj[i]['c'])))/offset));
      }
      ctx.lineTo(i*3, Math.floor(flatOff+(max-(parseFloat(props.cur['c'])))/offset));

      ctx.strokeStyle = '#e8b923'
      ctx.stroke();
    } catch (error) {
      console.error(error);
    }
    
  }

  useEffect(() => {
    const canvas = canvasRef.current
    const context = canvas.getContext('2d')
    
    drawline(context)
  }, [drawline])
  
  return <canvas ref={canvasRef} {...props}/>
}

export default Canvas