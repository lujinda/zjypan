String.format = function(src){
    if (arguments.length == 0)
        return null;
    var args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};
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

$(document).ready(function(){
    $('#input_key_wrap form').submit(function (event){
        $.post("", 
            {'file_key':$('.input_key_dir .input_key').val()},
            function (data){
                alert(data);
            });

        // 禁止默认事件的发现
        event.preventDefault();
        return false;
    });
    $('#input_key_wrap .btn_submit_key').click(function (event){
        $('#input_key_wrap .btn_submit_key').submit();
        event.preventDefault();
    });
});
