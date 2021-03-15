const express = require("express");
const router = express.Router();
const ws = require('ws');

router.get("/", (req, res) => {
  const client = new ws('wss://stream.binance.com:9443/ws/btcusdt@kline_1m');

  client.on('open', () => {
    
    client.send('Hello');
  });
  
  res.send({ response: "I am alive" }).status(200);
});

module.exports = router;