var express = require('express');
var router = express.Router();
const {spawn} = require('child_process');
fs = require('fs');

router.post('/', function(req, res, next) {

  //console.log(req.body.post)
  var dataToSend;
  console.log('in back')
  // spawn new child process to call the python script
  const python = spawn('python',  ['./python/getTransByDate.py', req.body.post ]);
  // collect data from script
  python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
  });
  // in close event we are sure that stream from child process is closed
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    // send data to browser
    //console.log(typeof(dataToSend))
    if (typeof(dataToSend) === 'string'){
      dataToSend = dataToSend.replace(/'/g, "\"")
    }
    res.send(dataToSend)
  });
  
}); 

module.exports = router;