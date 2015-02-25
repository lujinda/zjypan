$(document).ready(function(){
    requestInventory();
});

function requestInventory() {
    var host = 'wss://' + get_ws_host() +'/monitor'; // 通过nginx反向代理

    var websocket = new WebSocket(host);

    websocket.onopen = function (evt) {show_success('WebSocket已连接')};
    websocket.onmessage = function(evt) {
        if (evt['data']){
            var data = $.parseJSON(evt['data']);
            append_monitor_log(data['fileno'], 
                    data['log']);
        }
    };
    websocket.onerror = function (evt) {show_error('WebSocket连接失败'); return false;};
    websocket.onclose = function (evt){show_warning('WebSocket连接已断开'); return false;};
}

function append_monitor_log(fileno, log){
    var log_wrap = $('#log_monitor_wrap');
    $t = $('<li>' + log + '</li>'); // 临时的日志元素
    if (fileno == 2){
        $t.addClass('error_log');
    }
    log_wrap.append($t);
}

function get_ws_host(){
    return [document.location.hostname, document.location.port || (document.location.protocol == 'http' && 80 || 443)].join(':');
}

