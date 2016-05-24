var express = require('express'),
    swig = require('swig'),
    axios = require('axios');

var host = process.env["HOST_IP"]
var etcdEndpoint = 'http://' + host + '/proxy_info'

var app = express();

// This is where all the magic happens!
app.engine('html', swig.renderFile);

app.set('view engine', 'html');
app.set('views', __dirname + '/../views');
app.use('/static', express.static(__dirname + '/../public'));

app.set('view cache', false);
swig.setDefaults({
    cache: false
});

app.get('/', function(req, res) {
    console.log("GET" + etcdEndpoint)
    axios.get(etcdEndpoint)
        .then(function(response){
            console.log(response.data)
            res.render('index', {data: response.data, host});
        })
        .catch(function(e) {
            res.status(500)
            res.end(e.message)
        })

});

app.listen(3000, function() {
    console.log('Application Started on http://localhost:3000/');
});
