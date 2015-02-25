String.format = function(src){
    if (arguments.length == 0)
        return null;
    var args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};

function time_add_zero(time){
    return time < 10 ? '0' + time: time
}

function DateToString(seconds){
    d = new Date(seconds * 1000);
    return String.format("{0}-{1}-{2} {3}:{4}:{5}", d.getFullYear(),
            time_add_zero(d.getMonth()), time_add_zero(d.getDate()), 
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

