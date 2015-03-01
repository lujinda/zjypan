function list_share_file(api_url){
    $.ajax({dataType: 'json',
    url: api_url,
    type: 'GET',
    success: function(response){
        $('#share_box_wrap').empty();
        if (response['error']){
            return;
        }
        share_obj_list = response['result'];

        for (i in share_obj_list){
            $box = $('<div class="share_box"><div class="box_header"></div><div class="box_main"></div><div class="box_footer"></div></div>');
            write_share_box($box, share_obj_list[i]);
            $box.appendTo('#share_box_wrap').fadeIn(250 * i);
        }
    },
    error: function(){
        show_error_mess('获取文件列表失败，请刷新重试');
    },
    });
}

function write_share_box($box, share_obj){
    $box.find('.box_header').html(share_obj['file_name']);
    $box.find('.box_main').html(share_obj['share_decription']);
    $box.find('.box_footer').html(DateToString(share_obj['share_time']));
}
function _show_top_mess(type, mess){
    mess_map = {'warn': 'alert', 'success': 'alert alert-success', 'error': 'alert alert-error'};
    $('#top_box').find('span').html(mess).attr('class', mess_map[type])
        .fadeIn(250).fadeOut(5000);
}
function show_error_mess(mess){
    _show_top_mess('error', mess);
}


function show_success_mess(mess){
    _show_top_mess('success', mess);
}
function show_warn_mess(mess){
    _show_top_mess('warn', mess);
}
