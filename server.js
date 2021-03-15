const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const INDEX = '/index.html'
const socketIO = require('socket.io');
const ws = require('ws');
const {spawn} = require('child_process');

const app = express();
const port = process.env.PORT || 5000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var getKline = require('./routes/getKline');
app.use('/api/get-kline-data', getKline);
var getMline = require('./routes/getMline');
app.use('/api/get-margin-lines', getMline);
var wsBalance = require('./routes/getBalance');
app.use('ws/get-balance', wsBalance)


if(true){
//if (process.env.NODE_ENV === 'production') {
  // Serve any static files
  app.use(express.static(path.join(__dirname, 'frontend/build')));
    
  // Handle React routing, return all requests to React app
  app.get('*', function(req, res) {
    res.sendFile(path.join(__dirname, 'frontend/build', 'index.html'));
  });
}

const server = require('http').createServer(app);
const io = socketIO(server);

server.listen(port, () => console.log(`Listening on port ${port}`));

var balance = 0.0;

io.on('connection', (socket) => {
  console.log('Client connected');

  var transData = {};
  const python = spawn('python',  ['./python/getBalance.py']);
  python.stdout.on('data', function (data) {

    transData = JSON.parse(data.toString().replace(/'/g, "\""));
  });

  const client = new ws('wss://stream.binance.com:9443/ws/btcusdt@kline_1m');

  client.on('message', msg => {
    let transLen =Object.keys(transData).length
    //console.log(transLen)
    if (transLen && transLen < 5){
      balance = parseFloat(JSON.parse(msg).k.c)*transData.BTCbought
    }else if (transLen){
      balance = transData.sell.price*transData.BTCbought
    }
  });
  
  socket.on('disconnect', () => console.log('Client disconnected'));
  socket.on('time', function(timeString) {
    el = document.getElementById('server-time')
    el.innerHTML = 'Server time: ' + timeString;
  });
});

setInterval(() => io.emit('bal', balance), 1000);