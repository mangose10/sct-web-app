var express = require('express');
var router = express.Router();
const {spawn} = require('child_process');

router.get('/', function(req, res, next) {
  var dataToSend;

  const python = spawn('python',  ['./python/getMline.py']);
  python.stdout.on('data', function (data) {
    //console.log('Pipe data from python script ...');
    dataToSend = data.toString();
  });
  
  python.on('close', (code) => {
    //console.log(`child process close all stdio with code ${code}`);
    res.send(dataToSend)
  });
  
});

module.exports = router;