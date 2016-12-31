var http = require('http');
var server = http.createServer().listen(3000, function(){
  console.log('listening on *:3000');
});
var io = require('socket.io').listen(server);
var querystring = require('querystring');

io.on('connection',function(socket) {
    console.log('Connected to the client');

    socket.on('send message',function(data) {
        var values = querystring.stringify(data);

        var options = {
            host:'localhost',
            port: 8000,
            path:'/chat/message/save/',
            method:'POST',
            headers:{
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            }
        };

        var request = http.request(options, function(response) {
            response.setEncoding('utf8');
            response.on('data',function(data){
                //Here return django
                io.emit('receive message',data);
            });
        });

        request.write(values);
        request.end();
    });
});
