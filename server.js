const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var getKline = require('./routes/getKline');
app.use('/api/get-kline-data', getKline);
var getMline = require('./routes/getMline');
app.use('/api/get-margin-lines', getMline);
var getMline = require('./routes/getTransData');
app.use('/api/get-trans-by-date', getMline);


if(true){
//if (process.env.NODE_ENV === 'production') {
  // Serve any static files
  app.use(express.static(path.join(__dirname, 'frontend/build')));
    
  // Handle React routing, return all requests to React app
  app.get('*', function(req, res) {
    res.sendFile(path.join(__dirname, 'frontend/build', 'index.html'));
  });
}

app.listen(port, () => console.log(`Listening on port ${port}`));
