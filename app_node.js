var fs = require('fs');
var http = require('http');
var https = require('https');

var SSL_KEY  = process.env.SSL_KEY  || "/etc/letsencrypt/live/manadream.net/privkey.pem";
var SSL_CERT = process.env.SSL_CERT || "/etc/letsencrypt/live/manadream.net/fullchain.pem";

var useHttps = false;
try {
  if (fs.existsSync(SSL_KEY) && fs.existsSync(SSL_CERT)) {
    useHttps = true;
  }
} catch(e) {}

var server;
if (useHttps) {
  console.log('Starting HTTPS server on port ' + (process.env.NODE_PORT || 3002));
  server = https.createServer({
    key: fs.readFileSync(SSL_KEY),
    cert: [fs.readFileSync(SSL_CERT)]
  });
} else {
  console.log('Starting HTTP server on port ' + (process.env.NODE_PORT || 3002) + ' (no SSL certs found)');
  server = http.createServer();
}
server.listen(process.env.NODE_PORT || 3002);

const io = require("socket.io").listen(server);

var logger = require('./logger');

io.sockets.on('connection',function(socket) {
	console.log('user connected!');
        logger.request.info('user connected');

	socket.on('foo', function (data) {
	  console.log('here we are in action event and data is: ' + data);
	});

	socket.on('action', function (data) {
		console.log(data.mode);
                logger.request.info(data.mode);
		io.sockets.emit("action", {mode: data.mode,room: data.room});
		});

	// メッセージを受け取った時の動作
	  socket.on("message", function (data) {
	    // 全員に受け取ったメッセージを送る
	    io.sockets.emit("message", {value: data});
	  });
});

console.log('running ..');
