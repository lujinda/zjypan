var offset = 0;

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
        'stop_info': $('#settings_stop_info').val()};
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
                $('#top_error_mess p').html(data['mess']);
                $('#top_error_mess').show().fadeOut(4000);
            }else{
                $('#top_success_mess p').html(data['mess']);
                $('#top_success_mess').show().fadeOut(2000);
            }
        },
        error:function (){
            $('#top_error_mess p').html('保存失败');
            $('#top_error_mess').show().fadeOut(3000);
        },
        
    });
}

function settings_save(obj){
    $.get('/api/mailcode?t=' + (new Date().valueOf())); // 加一个时间，防止浏览器缓存
    $('#send_mail_code_wrap #mail_code').val('');
    $('#send_mail_code_wrap').modal({
        relatedTarget: this,
    onConfirm: function(e) {
        _post_settings(obj);
    },
    onCancel: function(e) {
        return false;
    }
    });
}

function check_settings_account_input(){
    $('#btn_settings_save').attr('disabled', true);
    if ($('#settings_username').val().trim() == '' || $('#settings_password_o').val().trim() == '' || $('#settings_password').val().trim() == '')
        return false;
    if ($('#settings_password').val().trim() == $('#settings_password_a').val().trim()){
        $('#btn_settings_save').attr('disabled', false);
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
