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

function post_settings_before(obj){ // 收集post数据
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

    if (obj == 'share'){
        data = {'page_limit': $('#settings_page_limit').val()};
    }
    if (obj == 'key_add' || obj == 'key_del'){
        data = {'key': $('#settings_key').val(),
        'operation': obj.split('_')[1]};
    }

    if (obj == 'key_madd'){
        data = {'key_list': $('#settings_key_list').val(),
        'operation': 'madd'};
    }

    if (obj == "vip_add" || obj == "vip_del"){
        data = {'vip': $('#settings_vip').val(),
        'operation': obj.split('_')[1]};
    }


    if (obj.indexOf('_') > 0){  //  如果obj带有了_，则将_前的第一个作为url请求对象
        obj = obj.split('_')[0];
    }

    url = '/tuxpy/settings/' + obj;

    data['mail_code'] = $('#mail_code').val();
    post_settings_ing(url, data);
}


function post_settings_ing(url, data){
    $.ajax({url: url,
        type:'POST',
        data:data,
        success:function (data){
            if (data['error']){
                show_error(data['mess']);
            }else{
                show_success(data['mess']);
                // 每次处理完请求后，再做一些界面上的设定
                if (data['set_obj'] == 'vip'){
                    opera_vip_list(data);
                }
            }
        },
        error:function (){
            $('#top_error_mess p').html('操作失败');
            $('#top_error_mess').show().fadeOut(3000);
        },
        
    });
}
function del_vip(vip){
    $('#settings_vip').val(vip);
    settings_save('vip_del');
}

function opera_vip_list(data){ // 在完成vip账号添加或删除完后调用的
    $('#settings_vip').val('');
    vip_func_map = {'add': append_vip_list, 'del': remove_vip_list}
    vip_func = vip_func_map[data['operation']];
    vip_func(data['vip']);
}

function append_vip_list(vip){
    $('#vip_list ul').append(String.format('<li id="vip_{0}"><span>{1}</span><span onclick="del_vip(\'{2}\')" class="am-badge am-badge-danger">DEL</span></li>', vip, vip, vip)); // 添加一个vip用户
    incr_vip_counts(1);
}

function remove_vip_list(vip){
    $('#vip_list #vip_' + vip).fadeOut(200).remove();
    incr_vip_counts(-1);
}

function incr_vip_counts(amount){
    var amount = amount || 1;
    var vip_counts_obj = $('#vip_list #vip_counts');
    vip_counts_obj.html(incr(vip_counts_obj.html(), amount));
}

function incr(i, amount){
    var amount = amount || 1;
    return parseInt(i) + amount;
}

function show_error(mess){
    $('#top_error_mess p').html(mess);
    $('#top_error_mess').show().fadeOut(4000);
}
function show_success(mess){
    $('#top_success_mess p').html(mess);
    $('#top_success_mess').show().fadeOut(2000);
}

function show_warning(mess){
    $('#top_warning_mess p').html(mess);
    $('#top_warning_mess').show().fadeOut(2000);
}


function settings_save(obj){
    $.get('/api/mailcode?t=' + (new Date().valueOf())); // 加一个时间，防止浏览器缓存
    $.ajax({url: '/api/mailcode?t=' + (new Date().valueOf()),
        type:'GET',success:function (data){
            if (data){
                post_settings_before(obj);
            }else{
                $('#send_mail_code_wrap #mail_code').val('');
                $('#send_mail_code_wrap').modal({
                    relatedTarget: this,
                    closeViaDimmer:false,
                    onConfirm: function(e) {
                        post_settings_before(obj);
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



function settings_save(obj){
    $.get('/api/mailcode?t=' + (new Date().valueOf())); // 加一个时间，防止浏览器缓存
    $.ajax({url: '/api/mailcode?t=' + (new Date().valueOf()),
        type:'GET',success:function (data){
            if (data){
                post_settings_before(obj);
            }else{
                $('#send_mail_code_wrap #mail_code').val('');
                $('#send_mail_code_wrap').modal({
                    relatedTarget: this,
                    closeViaDimmer:false,
                    onConfirm: function(e) {
                        post_settings_before(obj);
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
function check_post(event){
    if ($('#post_title').val().trim() == ''){
        show_error('标题不能为空哦');
        event.preventDefault();
        return false;
    }
}

function check_all(s){
    $('.checkbox').attr('checked', s);
}
function do_operation(operation, $form){
    if ($('.checkbox:checked').length  == 0){
        alert('啥都没选中！');
        return;
    }
    if (operation == 'del'){
        if (! confirm('确定要删除吗'))
            return;
    }
    $form.attr('action', '?action=' + operation).submit();
}
function do_post(operation){
    do_operation(operation, $('#list_post_form'));
}

function do_feedback(operation){
    do_operation(operation, $('#list_feedback_form'));
}

function key_flush(){
    $('#confirm_msg_wrap').modal({
        relatedTarget: this,
        onConfirm: function(options) {
            request_api('/tuxpy/settings/key', 'POST',{'operation': 'flush'});
        },
        onCancel: function() {
            return false;
        }
    });
}
