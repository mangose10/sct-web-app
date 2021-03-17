import React, { useRef, useEffect } from 'react'
import useMousePosition from './mousePosition'
import ThreeDotsWave from './loading'
import './../css/loader.css'
import useWindowDimensions from './windowDimensions'

const Canvas = props => {

  const canvasRef = useRef(null)
  const { x, y } = useMousePosition();
  const { height, width } = useWindowDimensions();

  var obj
  var max
  var min
  var offset
  var flatOff
  var lineWidth
  var center

  const hover = ctx => {
    ctx.beginPath()
    ctx.strokeStyle = "#000"
    var scrollOffset = width < canvasRef.current.width ? document.scrollingElement.scrollLeft : 0;
    let xMagnet = Math.floor((x-canvasRef.current.offsetLeft+scrollOffset)/lineWidth)*lineWidth + center
    let yRangeStart = canvasRef.current.offsetTop

    if (y > yRangeStart && y < (yRangeStart + canvasRef.current.height)){
      ctx.moveTo(xMagnet, 0)
      ctx.lineTo(xMagnet, canvasRef.current.height)
      ctx.stroke()
      ctx.closePath()
    }
  }

  const drawline = ctx => {
    obj = props.data
    max = obj.max;
    min = obj.min;
    offset = ((max-min)/canvasRef.current.height)/0.7;
    flatOff = (canvasRef.current.height - (max-min)/offset)/2;
    
    
    ctx.clearRect(0,0,canvasRef.current.width,canvasRef.current.height);
    ctx.fillStyle = "#333";
    ctx.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height); 
    //console.log(props.margin)
    if (Object.keys(props.margin).length < 2){
      
    }else{
      ctx.beginPath();
      let buyHeight = Math.floor(flatOff+(max-props.margin['buy']['price'])/offset);
      ctx.moveTo(0, buyHeight);
      ctx.lineTo(canvasRef.current.width-1, buyHeight);
      
      
      ctx.strokeStyle = '#fff';
      ctx.fillStyle = "#fff";
      ctx.stroke();
      ctx.closePath();
    
      ctx.font = '12px monospace'
      ctx.fillStyle = "#fff";
      ctx.fillText('Buy price: ' + (props.margin.buy.price), 10, 20);

      ctx.beginPath();
      let sellPrice = props.margin.break/props.margin.BTCbought;
      let sellHeight = Math.floor(flatOff+(max-sellPrice)/offset);

      ctx.moveTo(0, sellHeight);
      ctx.lineTo(canvasRef.current.width, sellHeight);

      ctx.strokeStyle = "#e69500";
      ctx.fillStyle = "#e69500";
      ctx.stroke();
      ctx.closePath();
    }

    obj = obj.klinedata;
    lineWidth = Math.floor(canvasRef.current.width/120)
    center = (lineWidth/2) - 1
    ctx.lineWidth = lineWidth % 2 === 0 ? 2 : 1
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
      
      ctx.rect(i*lineWidth, Math.floor(flatOff+(max-(parseFloat(obj[i][start])))/offset), lineWidth-1, Math.floor(Math.abs(parseFloat(obj[i]['o'])-parseFloat(obj[i]['c']))/offset));
      ctx.stroke()
      ctx.fill()
    }
    
    let color = parseFloat(props.cur['o']) > parseFloat(props.cur['c']) ? red : green;
    
    ctx.beginPath()
    ctx.moveTo((i*lineWidth)+center, Math.floor(flatOff+(max-(parseFloat(props.cur['h'])))/offset))
    ctx.lineTo((i*lineWidth)+center, Math.floor(flatOff+(max-(parseFloat(props.cur['l'])))/offset))
    ctx.strokeStyle = color
    ctx.stroke()
    ctx.closePath()

    ctx.strokeStyle = "#000"
    ctx.stroke();
    ctx.closePath()

    let start = parseFloat(props.cur['o']) > parseFloat(props.cur['c']) ? 'o' : 'c';
    ctx.fillStyle = color
    ctx.rect(i*lineWidth, Math.floor(flatOff+(max-(parseFloat(props.cur[start])))/offset), lineWidth-1, Math.floor(Math.abs(parseFloat(props.cur['o'])-parseFloat(props.cur['c']))/offset));
    ctx.stroke()
    ctx.fill()

    let selected = Math.floor((x-canvasRef.current.offsetLeft)/lineWidth)
    let pixelLength = 3
    let selectedObj = (selected < Object.keys(obj).length) && selected >= 0 ? {
      'l':obj[selected]['l'],
      'o':obj[selected]['o'],
      'c':obj[selected]['c'],
      'h':obj[selected]['h']
    } : selected === Object.keys(obj).length ? {
      'l':props.cur['l'],
      'o':props.cur['o'],
      'c':props.cur['c'],
      'h':props.cur['h']
    } : {
      'l':0,
      'o':0,
      'c':0,
      'h':0
    };

    let valText = "low: " + selectedObj.l + " open: " + selectedObj.o + " close: " + selectedObj.c + " high: " + selectedObj.h;
    ctx.fillStyle = "#e200e2"
    ctx.font = '12px monospace'
    ctx.fillText(valText, canvasRef.current.height - (valText.length) - 10, 20)
    
  }

  useEffect(() => {
    var loader = document.querySelectorAll('.loader');
    var hideLoader = () => {}
    if (loader){
      hideLoader = () => {
        for (var i = 0; i < loader.length;i++){
          loader[i].classList.add('loaderhide');
          loader[i].classList.remove('loader');
          loader[i].classList.remove('loaderContainer');
        }
      }
    }
    const canvas = canvasRef.current
    while (canvas == null){}
    const context = canvas.getContext('2d')

    if (Object.keys(props.data).length){
      hideLoader()
      drawline(context)
      hover(context)
    }
  }, [drawline, hover])
  
  return (
    <div>
      <div>
        <ThreeDotsWave />
      </div>
      <canvas ref={canvasRef} {...props}/>
    </div>
  );
}

export default Canvas