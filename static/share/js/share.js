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
        if (share_obj_list.length == 0){
            show_warn_mess('无符合条件的文件');
            return;
        }

        for (i in share_obj_list){
            $box = $('<div class="share_box"><div class="box_header"><a target="_blank"></a></div><div class="box_main"></div><div class="box_footer"><span class="share_time"></span><div class="share_file_h_c"><a class="share_up"><i class="icon-thumbs-up"></i> <span class="up_num"></span></a><a class="share_down"><i class="icon-thumbs-down"></i> <span class="down_num"></span></a></div><a class="share_file_down" target="_blank">下  载</a></div></div>');
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
    $box.find('.box_header a').html(share_obj['file_name']);
    $box.find('.box_main').html(share_obj['share_decription']);
    $box.find('.box_footer .share_time').html(DateToString(share_obj['share_time']));
    $box.find('.box_footer .up_num').html(share_obj['up_num']);
    $box.find('.box_footer .share_up').attr('onclick', 'add_share_up_num("' + share_obj['share_id'] + '", this)');
    $box.find('.box_footer .down_num').html(share_obj['down_num']);
    $box.find('.box_footer .share_down').attr('onclick', 'add_share_down_num("' + share_obj['share_id'] + '", this)');
    $box.find('.box_footer .share_file_down').attr('href', share_obj['share_url'] + '?attname=' + share_obj['file_name']);
}
function _show_top_mess(type, mess){
    mess_map = {'warn': 'alert', 'success': 'alert alert-success', 'error': 'alert alert-error'};
    $('#top_box').attr('class', mess_map[type]).fadeIn().find('span').html(mess);
    $('#top_box').fadeOut(2000);
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

function __add_up_num(type, share_id){
    var url = '/share/' + type;
    $.ajax({
        type: 'GET',
        url: url,
        dataType: 'json',
        data: {'share_id': share_id},
        success:function (response){
            if (response['error']){
                show_warn_mess(response['error']);
                return;
            }
        },
        error:function(){
                show_error_mess('点评失败，请重试');
        },
    });
}

function add_share_up_num(share_id, obj){
    __add_up_num('up', share_id);
    $(obj).attr('onclick', '').html('已顶');
    return false;
}

function add_share_down_num(share_id, obj){
    __add_up_num('down', share_id);
    $(obj).attr('onclick', '').html('已踩');
    event.preventDefault();
}
