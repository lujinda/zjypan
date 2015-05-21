String.format = function(src){
    if (arguments.length == 0)
        return null;
    var args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};

function disable_obj($obj){
    $obj.addClass('disable');
}
function get_cookie(name){
    var c = document.cookie.match("\\b" + name + "=\"?([^;]*)\\b");
    return c ? c[1] : '';
}

function del_cookie(name){
    var exp = new Date();
    exp.setTime(exp.getTime() - 1000);
    var cookie = get_cookie(name);
    if (cookie){
        document.cookie = name + '=' + cookie + ";expires=" + exp.toGMTString();
    }
}

function time_add_zero(time){
    return time < 10 ? '0' + time: time
}

function DateToString(seconds){
    d = new Date(seconds * 1000);
    return String.format("{0}-{1}-{2} {3}:{4}:{5}", d.getFullYear(),
            time_add_zero(d.getMonth() + 1), time_add_zero(d.getDate()), 
            time_add_zero(d.getHours()), time_add_zero(d.getMinutes()), time_add_zero(d.getSeconds()));
}

function update_code_img(){
    // 防止浏览器缓存
    var url = '/code.py?token=' + $('#token').val() + '&t=' + (new Date().valueOf());
    $('#code_img').attr('src', url);
}
function show_post_list(limit, skip){
    limit = typeof limit == 'number' ? limit: 1;
    skip = typeof skip == 'number' ? skip : 0;
    $.ajax({
        url: '/api/post',
        dataType: 'json',
        data:{'limit': limit, 'skip': skip},
        success:function(data){
            if (data['error'] == ''){
                if (limit == 1){ // 如果只有一条，表示是在首页显示的
                    post = data['result'][0];
                    $('#top_post_index span').html(post['post_title']);
                    write_post_box($('#post_box_index'), post);
                }else{
                    post_list = data['result'];
                    for (i in post_list){
                        $box = $('<div class="post_box"><div class="post_box_title"></div><div class="post_box_content"></div><div class="post_box_footer"></div></div>');
                        write_post_box($box, post_list[i]);
                        $box.appendTo('#post_box_list').fadeIn(250 * i);
                    }
                }
            }else{
                return [];
            }
        },
        error:function(data){
            return [];
        },
    });
}
function write_post_box($box, post){
    $box.find('.post_box_title').html(post['post_title']);
    $box.find('.post_box_content').html(post['post_content']);
    $box.find('.post_box_footer').html(DateToString(post['post_time']));
}

function show_all_post(){
    $('#header, #main, #footer').hide();
    $('body').css('background-color', '#eee');
    $post_box_list = $('<div id="post_box_list"></div>');
    $('body').append($post_box_list);
    show_post_list(0, 0);
    $('html').click(function(){
        $post_box_list.remove();
        $('body').css('background-color', '#fff');
        $('#header, #main, #footer').fadeIn(200);
    });
}

function submit_feedback(){
    var content = $('#feedback_content').val();
    var contact = $('#feedback_contact').val();

    if (! (content && contact)){
        alert('请把相关信息输入完毕');
        return;
    }

    $.ajax({
        dataType:'json',
        type:'POST',
        url:'/api/feedback',
       data:{'content': content,
        'contact': contact},
        success: function(response){
            alert(response['result']);
            $('.msg_wrap').fadeOut(250);
        },
        error: function(){
            alert('不好意思，评论失败');
        }
    });
}
function show_last_upload(){
    var last_upload = decodeURI(get_cookie('last_upload'));
    if (!last_upload){
        $('#footer_tips').hide().find('#last_upload_key').html('');
        return;
    }
    $('#footer_tips').show().find('#last_upload_key').html(last_upload);
}

function del_last_upload(){
    del_cookie('last_upload');
    show_last_upload();
}

