//
// # SimpleServer
//
// A simple chat server using Socket.IO, Express, and Async.
//
var http = require('http');
var express = require('express');
var url=require('url')
//
// ## SimpleServer `SimpleServer(obj)`
//
// Creates a new instance of SimpleServer with the following options:
//  * `port` - The HTTP port to listen on. If `process.env.PORT` is set, _it overrides this value_.
//
var app = express();
app.configure(function() {
  app.use(app.router);
  app.use(express.static(__dirname + '/web'));
});
var rpc = require('node-json-rpc');
var options = {
  port: 7000,
  host: '127.0.0.1',
  path: '/',
  strict: true
};
var client = new rpc.Client(options);
app.get('/introns',function(req,res){
        var url_param = url.parse(req.url,true);
	var m=req.gene || url_param.query.gene;
        client.call(
                {"jsonrpc":"2.0","method": "introns", "params": [m],"id":m},
        function (err, res2) {
    		if (err) { console.log("error",err); }
    		else { res.json(res2)}
     	}
   );
});
app.get('/predict',function(req,res){
        var url_param = url.parse(req.url,true);
	var m=req.seq || url_param.query.seq;
        client.call(
                {"jsonrpc":"2.0","method": "branch", "params": [m],"id":m},
        function (err, res2) {
    		if (err) { console.log("error",err); }
    		else { res.json(res2)}
     	}
   );
});




app.listen(8080)
