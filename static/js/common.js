String.format = function(src){
    if (arguments.length == 0)
        return null;
    var args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};
function down_file(){
    $('.file_operation form').attr('action', '/file.py').submit();
}
function del_file(){
    if (!confirm("确定要删除 " + $('#file_name').html())){
        return;
    }
    $.ajax({type:'DELETE', url:'/file.py', 
        data:{'file_key': $('#file_key').val()},
        success:function(data){
            window.location.reload();
        }
    });
}
function DateToString(seconds){
    d = new Date(seconds * 1000);
    return d.toLocaleString();
}
function show_err_message(error){
    $('.file_percent').css({'background-color': 'red',
        'width':'100%'});
    $('.file_percent').html(error);
}
function show_succ_message(file_key){
    $('.file_percent').css({'background-color': '#47CF00', 'color':'#000', 'line-height':'100%'});
    $('.file_percent').html(String.format(
                '<div class="file_key_mess">您的文件代码是:<span class="file_key">{0}</span></div><div class="file_key_tip">文件代码由日期+星期+随机两位字母组成</div>', file_key));
}

function update_code_img(){
    // 防止浏览器缓存
    var url = '/code.py?token=' + $('#token').val() + '&t=' + (new Date().valueOf());
    $('#code_img').attr('src', url);
}
