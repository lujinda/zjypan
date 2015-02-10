$(document).ready(function (){
    $('#login_form').submit(function (){
        $('#login_btn').click();
    });
    $('#login_btn').click(function(event){
        if (post_data_empty()){
            alert('请把登录信息都填写完成');
            return false;
        }else{
        $.ajax({
            type:'POST',
            data:{'username': $('#username').val(),
            'password': $('#password').val(),
            'code': $('#code').val(),
            'token': $('#token').val()},
            error:function(){
                alert('登录出错，请刷新重试');
            },
            success:function(data){
                var error = data['error'];
                if (error){
                    $('#tip').html(data['error']);
                    $('#code_img').click();
                }else{
                    window.location.href=data['url'];
                }
            },
        });
        }
        event.preventDefault();
    });
});
function post_data_empty(){
    var all_empty = false;
    $('#login_wrap input').each(function (){
        if ($(this).val().trim() == ''){
            all_empty = true;
            $(this).css('border-color', 'red').focus();
        }
    });
    return all_empty;
}
