$(document).ready(function(){
    setTimeout(requestInventory, 100);
});

function requestInventory() {
    var host = 'wss://admin.tuxpy.info/monitor'; // 通过nginx反向代理

    var websocket = new WebSocket(host);

    websocket.onopen = function (evt) { };
    websocket.onmessage = function(evt) {
        $('body').append('<p>' + evt['data'] + '</p>');
    };
    websocket.onerror = function (evt) { };
}

