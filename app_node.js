var io   = require('socket.io').listen(3002);

io.sockets.on('connection',function(socket) {
	console.log('user connected!');

	socket.on('foo', function (data) {
	  console.log('here we are in action event and data is: ' + data);
	});
	
	socket.on('action', function (data) {
		console.log(data.mode);
		io.sockets.emit("action", {mode: data.mode,room: data.room});
		});

	// メッセージを受け取った時の動作
	  socket.on("message", function (data) {
	    // 全員に受け取ったメッセージを送る
	    io.sockets.emit("message", {value: data});
	  });
});

console.log('running ..');
