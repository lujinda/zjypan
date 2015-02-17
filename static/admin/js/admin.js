var offset = 0;
var log_api_url = '';
function load_more_operation($btn){
    var limit = 10;
    $.ajax({type:'GET',
        url:'/api/operation',
        data:{'offset': offset, 'limit': limit},
        success:function(data){
            if (data['error'] =='' && data['result'].length > 0){
                offset += limit;
                append_operation_list(data['result']);
                $btn.button('reset');
            }else{
                $btn.button('loading').val('全部加载完成');
            }
        },
        error:function(){
                $btn.button('reset').val('加载失败');
        }
    });
}

function append_operation_list(operation_list){
    for (i in operation_list){
        var operation = operation_list[i];
        var tr_e = $(String.format('<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>',
                operation['operation'], operation['UA'], operation['ip'], DateToString(operation['time'])));
        tr_e.hide().fadeIn(500).attr('style', '').appendTo($('#operation_list'));
    }
}

function _post_settings(obj){
    url = '/tuxpy/settings/' + obj;
    if (obj == 'global'){
        data = {'up_time_interval': $('#settings_up_time_interval').val(),
        'up_num': $('#settings_up_num').val(), 
        'stop': $('#settings_stop').attr('checked') ? 'on': 'off',
        'stop_info': $('#settings_stop_info').val(),
        'verify': $('#settings_verify').attr('checked') ? 'on': 'off',
        };
    }

    if (obj == 'account'){
        data = {'username': $('#settings_username').val(),
            'password': $('#settings_password').val(),
            'old_password': $('#settings_password_o').val(),
        };
    }

    if (obj == 'file'){
        data = {'expired_day': $('#settings_expired_day').val(),
                'add_expired_day': $('#settings_add_expired_day').val(),
        };
    }

    data['mail_code'] = $('#mail_code').val();

    $.ajax({url: url,
        type:'POST',
        data:data,
        success:function (data){
            if (data['error']){
                show_error(data['mess']);
            }else{
                show_success(data['mess']);
            }
        },
        error:function (){
            $('#top_error_mess p').html('保存失败');
            $('#top_error_mess').show().fadeOut(3000);
        },
        
    });
}

function show_error(data){
    $('#top_error_mess p').html(data);
    $('#top_error_mess').show().fadeOut(4000);
}
function show_success(data){
    $('#top_success_mess p').html(data);
    $('#top_success_mess').show().fadeOut(2000);
}


function settings_save(obj){
    $.get('/api/mailcode?t=' + (new Date().valueOf())); // 加一个时间，防止浏览器缓存
    $.ajax({url: '/api/mailcode?t=' + (new Date().valueOf()),
        type:'GET',success:function (data){
            if (data){
                _post_settings(obj);
            }else{
                $('#send_mail_code_wrap #mail_code').val('');
                $('#send_mail_code_wrap').modal({
                    relatedTarget: this,
                    closeViaDimmer:false,
                    onConfirm: function(e) {
                        _post_settings(obj);
                    },
                    onCancel: function(e) {
                        return false;
                    }
                });

            }
        }});

}
function check_settings_account_input(){
    $('#btn_settings_save').attr('disabled', true);
    if ($('#settings_username').val().trim() == '' || $('#settings_password_o').val().trim() == '' || $('#settings_password').val().trim() == '')
        return false;
    if ($('#settings_password').val().trim() == $('#settings_password_a').val().trim()){
        $('#btn_settings_save').attr('disabled', false);
    }
}

function request_api(url, method, data, success, error){ // 用来处理api访问 
    data = data || {};
    method = method || 'GET';
    $.ajax({
        url: url, 
        type: method,
        data: data,
        success:function(data){
            if (data['error'] != ''){
                show_error(data['error']);
            }else if (success){
                success(data['result']);
            }else{
                show_success('操作成功');
            };
        },
        error:function(){
            show_error('操作失败');
        },
    });
    
}

function clear_operation(){
    $('#confirm_msg_wrap').modal({
        relatedTarget: this,
        onConfirm: function(options) {
            request_api('/api/operation', 'DELETE');
        },
        onCancel: function() {
            return false;
        }
    });
}

function flush_cache(){
    request_api('/api/cache', 'DELETE');
}


function load_more_log($btn, log_key_list_map, log_type){
    var log_key_list = log_key_list_map[log_type.split('?')[0]];
    var limit = 20;
    $.ajax({url: log_api_url, 
        data:{'limit': limit, 'offset': offset},
    success:function(data){
        if (data['result'].length > 0){
            offset += limit;
            append_log_list(log_key_list, data['result'])
            $btn.button('reset');
        }else{
            $btn.button('loading').val('全部加载完成');
    }}});
}

function init_log_list_tbody(){
    $('#log_list_tbody').empty();
    offset = 0;
}

function append_log_list(log_key_list, log_list){
    for (i in log_list){
        var e_tr = $('<tr></tr>');
        log = log_list[i];
        for (var j=0; j < log_key_list.length; j++){
            log_key = log_key_list[j];
            log_value = log[log_key];
            if (log_key == 'time'){
                log_value = DateToString(log_value);
            }
            e_tr.append('<td>' + log_value + '</td>');
        }
        $('#log_list_tbody').append(e_tr);
    }
}

$(document).ready(function(){
    $(window).scroll(function(){
        if ($(this).scrollTop() > $(window).height() / 3){
            $('#goToTop').fadeIn(1000);
        }else{
            $('#goToTop').fadeOut(1000);
        }

    });
    $('#goToTop a').click(function (event){
        $('html, body').animate({scrollTop:0}, 'slow');
    });
});


