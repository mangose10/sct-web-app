import mongoose from "mongoose";

//const mongoose = require("mongoose")

function Chart() {
  let mongoDB = 'mongodb+srv://crespi:Simple1234@sctdb.v1k99.mongodb.net/test';
  mongoose.connect(mongoDB);
  mongoose.Promise = global.Promise;
  let db = mongoose.connection;

  //print(db['SCT']['candles']['m1'])
  
  return (
    <div className="Chart">
      
    </div>
  );
}

export default Chart;
