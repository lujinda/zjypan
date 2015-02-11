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
