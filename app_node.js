var fs = require('fs');
var opts = {
  key: fs.readFileSync("/etc/letsencrypt/live/manadream.net/privkey.pem"),
  cert: [fs.readFileSync("/etc/letsencrypt/live/manadream.net/cert.pem")],
};
const server = require("https").createServer(opts);
server.listen(3002);

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
