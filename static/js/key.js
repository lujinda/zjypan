function toggle_btn(e, obj){
    $(".divBtn").hide();
    e = window.event || e;
    var obj = e.srcElement || e.target;
    if (obj.tagName == 'LI')return;
    if($(obj).is("#key_list span")) {
        $("#key_list_child").slideUp();
    }

    $(obj).parent().find("div").slideToggle(200);
}
function list_child(obj){
    var file_key = $(obj).parent().prev().html();
    var $key_list_child = $('#key_list_child');
    $.ajax({
        url:'/api/key/' + file_key,
        type:'GET',
        success: function (response){
            var result = response['result'];
            var $wrap = $('#key_list_child ul').empty();
            for (var i in result){
                append_file_item($wrap, result[i]);
            }
        },
    });

    var step=$(obj).offset().top;
    $key_list_child.css({"top":step+"px","position":"absolute"}).slideToggle(200);
}


function show_all_key_list(){
    $.ajax({
        type: 'GET',
        url: '/api/key',
        success: function(response){
            var result = response['result'];
            var $wrap = $('#key_list ul');
            for (var i in result){
                append_key_item($wrap, result[i]);
            }
        }
    });
}
function append_key_item($wrap, data){
    var _key_item = key_item_template.clone();
    _key_item.click(function(e){
        toggle_btn(e, this);
    }).find('span').html(data);
    _key_item.find('.btn_list_child').click(function(){
        list_child(this);
    });
    _key_item.find('.btn_key_manager').attr('href', '/manage.py?file_key=' + data);
    _key_item.show().appendTo($wrap);

}

function append_file_item($wrap, data){
    var _file_item = file_item_template.clone();
    _file_item.click(function(e){
        toggle_btn(e, this);
    }).find('span').html(data['file_name']);
    _file_item.find('.btn_key_down').attr('href', data['file_url']);
    _file_item.fadeIn().appendTo($wrap);
}
$(document).ready(function(){
    key_item_template = $('#key_list .head_QQ_ul li').first();
    file_item_template = $('#key_list_child .head_QQ_ul li').first().clone();
    show_all_key_list();
});
