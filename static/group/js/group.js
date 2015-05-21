function show_error(message){
    var $obj = $('#top_error_message');
    $obj.html(message);
    __show_top_obj($obj);
}
function show_success(message){
    var $obj = $('#top_success_message');
    $obj.html(message);
    __show_top_obj($obj);
}

function __show_top_obj($obj){
    $obj.fadeIn(250).fadeOut(3000);
}

function send_ajax_manager(opera, success, data){
    data = data || {};
    $.ajax({
        url: '/group/manager?opera=' + opera,
        dataType: 'json',
        type: 'POST',
        data: data,
        success: function(response){
            var error = response['error'];
            if (error){
                show_error(error);
                return false;
            }
            success(response);
        },
        error: function(){
            show_error('系统出错了');
        },
    });
}

function refre_item_list(){
        $btn = $('#btn_refre_item_list');
        $btn.button('loading');
        success =  function(response){
            $('#group_list_wrap tbody').empty();
            var result = response['result'];
            var $tbody_obj = $('#group_list_wrap tbody')
            for (i in result){
                write_item_tr($tbody_obj, result[i]);
            }
            $('#btn_refre_item_list').button('reset');
        };
        send_ajax_manager('list', success);
}

function write_item_tr($tbody_obj, item_data){
    $tbody_obj.append(String.format("<tr><td class='item_name'>{0}</td><td class='item_email'>{1}</td><td><span class='label label-primary' onclick='edit_item(this)'>编辑</span>  <span onclick='del_item(this)' class='label label-danger'>删除</span> <input type='text' style='display:none' class='item_follow_events' value='{2}' /></td></tr>", item_data['item_name'],
                item_data['item_email'], item_data['follow_events'].join(';')));
}
function del_item(obj){
    if (!confirm('确定要删除该成员吗')){
        return;
    }
    $obj = $(obj);
    $td = $obj.parent();
    $tr = $td.parent();
    var item_email = $td.prev().html();
    var item_name = $td.prev().prev().html();
    var data = {'item_email': item_email};
    success = function(response){
            $tr.remove();
            show_success(String.format('{0} {1} 已从小组中移除', item_name, item_email));
        };
    send_ajax_manager('del', success, data);
}

function edit_item(obj){
    var $tr = $(obj).parent().parent();
    var item_name = $tr.find('.item_name').html();
    var item_email = $tr.find('.item_email').html();
    var follow_events_list = $tr.find('.item_follow_events').val().split(';');
    $form = $('#add_group_inputbox form'); // 编辑框的表单
    $form.find('#add_item_name_input').val(item_name);
    $form.find('#add_item_email_input').val(item_email).prop('readonly', true);
    $form.attr('action', $form.attr('action').split('=')[0] + '=edit');

    $form.find('.add_follow_events').removeProp('checked');
    for (i in follow_events_list){
        $form.find('#item_follow_' + follow_events_list[i]).prop('checked', true);
    }
    $('#add_group_inputbox').modal();
}

$(document).ready(function(){
    $('#add_group_inputbox').on('hidden.bs.modal', function(){
        var $form = $(this).find('form');
        $form.resetForm();
        $(this).find('#item_follow_upload').prop('checked', true);
        $(this).find('input').removeProp('readonly');
        $form.attr('action', $form.attr('action').split('=')[0] + '=add');
    });
    $('#add_group_item_btn').click(function(){
        var item_name_obj = $('#add_item_name_input');
        var item_email_obj = $('#add_item_email_input');
        var item_name = item_name_obj.val();
        var item_email = item_email_obj.val();
        if(!(item_name && item_email)){
            show_error('请把信息填写完哦');
            return false;
        }
        var reg_email =  /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+\.([\.a-zA-Z0-9_-])+$/;
        if (! reg_email.test(item_email)){
            show_error('输入的邮箱不合法哦');
            item_email_obj.val('').focus();
            return false;
        }
        $('#add_group_item_form').ajaxSubmit({
            dateType: 'json',
            success:function(response){
                var error = response['error'];
                if (error){
                    show_error(error);
                    return false;
                }
                var message = response['message'];
                if (item_email_obj.prop('readonly')){
                    refre_item_list();
                }
                show_success(message);
            },
            error: function(){
            show_error('系统出现未知错误');
            }
        });
        return false;
    });
});
