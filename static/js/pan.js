function down_file(obj){
    $(obj.parentNode).attr('action', '/file.py').submit();
}
function del_file(obj){
    var $wrap = $get_manage_wrap(obj);
    if (!confirm("确定要删除 " + $wrap.find('.file_name').html())){
        return;
    }
    $.ajax({type:'DELETE', url:'/file.py', 
        data:{'file_key': $wrap.find('.file_key').val(), 'file_name': $wrap.find('.file_name').val()},
        success:function(data){
            if ($('.manage_wrap').length > 1){
                $wrap.fadeOut(250);
                setTimeOut($wrap.remove, 400);
            }else{
                window.location.read();
            }
        },
        error:function (){
            alert('删除失败，请重试');
        }
    });
}


function show_share_msg(obj){
    $wrap = $get_manage_wrap(obj);
    $share_msg = $wrap.find(".share_msg");
    $share_msg.find('strong').html($wrap.find('.file_name').html());
    $share_msg.fadeIn(250);
}
function close_share_msg(obj){
    $wrap = $get_manage_wrap(obj);
    $wrap.find(".share_msg").hide();
}
function unshare(obj){
    $wrap = $get_manage_wrap(obj);
    var file_key = $wrap.find('.file_key').val();
    var file_name = $wrap.find('.file_name').val();
    if (!file_key)
        return;
    $.ajax({
        url: '/share/' + file_key,
        dataType: 'json',
        type: 'DELETE',
        data:{'file_key': file_key, 'file_name': file_name},
        error: function(){
            alert('系统出错，请重试');
        },
        success: function(response){
            change_share_btn($wrap);
        },
    });
}
function share_file(obj){
    var $wrap = $get_manage_wrap(obj);
    var file_key = $wrap.find('.file_key').val();
    if (!file_key)
        return;
    var description = $wrap.find('.share_description').val();
    $.ajax({
        url: '/share/' + file_key,
        dataType:'json',
        data:{'description': description, 
            'file_name': $wrap.find('.file_name').val()},
        type:'POST',
        error: function(){
            alert('共享出错，请重试');
        },
        success: function(response){
            if (response['error']){
                alert(response['error']);
            }else{
                change_share_btn($wrap, response['share_id']);
            }
        }
    });
}

function change_share_btn($wrap, share_id){
    if (share_id){
        $wrap.find('.btn_file_share').attr({'href': '/share_site', 'target': '_blank'}).removeAttr('onclick')
            .html('资源广场');
        $wrap.find('.btn_file_unshare').show();
        $wrap.find(".share_msg").hide();
    }else{
        $wrap.find('.btn_file_share').attr('onclick',"show_share_msg(this)").removeAttr('href')
            .html('共 享');
        $wrap.find('.btn_file_unshare').hide();
    }
}

function show_err_message(error){
    $('.file_percent').css({'background-color': 'red',
        'width':'100%'});
    $('.file_percent').html(error);
}
function show_succ_message(file_key){
    $('.file_percent').css({'width': '100%','background-color': '#47CF00', 'color':'#000', 'line-height':'100%'});
    $('.file_percent').html(String.format(
                '<div class="file_key_mess">您的文件代码是:<span class="file_key">{0}</span></div><div class="file_key_tip">文件代码由<strong>日期+常用成语或词语</strong>组成</div>', file_key));
}

function start_file_upload(){
        $filequeue = $(".file_form .filelist.queue");
        $filelist = $(".file_form .filelist.complete");
        
        $(".file_form .dropped").dropper({
            action: "/file.py",
            maxSize: 5242880, // 5 mb
            maxQueue: 1
        }).on("start.dropper", onStart)
        .on("complete.dropper", onComplete)
        .on("fileStart.dropper", onFileStart)
        .on("fileProgress.dropper", onFileProgress)
        .on("fileComplete.dropper", onFileComplete)
        .on("fileError.dropper", onFileError);

        
        $(window).one("pronto.load", function() {
            $(".file_form .dropped").dropper("destroy").off(".dropper");
        });
}

    function onStart(e, files) {
        $('.file_form').hide();
        $('.file_process').show();

    }

    function onComplete(e) {
        console.log("Complete");
        // All done!
    }

    function onFileStart(e, file) {
        $('.file_percent').css('width', '0%');
    }

    function onFileProgress(e, file, percent) {
        $('.file_percent').css({'width':percent + '%'});
    }

    function onFileComplete(e, file, response) {
        if (response['error']){
            show_err_message(response['error']);
        }else{
            show_succ_message(response['file_key']);
        }
    }

    function onFileError(e, file, error) {
        $('.file_percent').hide().fadeIn(500);
        show_err_message(error);
        setTimeout("window.location.reload()", 5000);
    }


function $get_manage_wrap(obj){
    return $(obj.parentNode.parentNode.parentNode);
}

function add_new_file(file){
    if (file.size > 5242880){
        alert('文件大小超过限制');
        return false;
    }
    var file_reader = new FileReader();
    var blob_slice = File.prototype.mozSlice || File.prototype.webkitSlice || File.prototype.slice;

    var chunk_size = 2097152;
    var chunks = Math.ceil(file.size / chunk_size);
    var current_chunk = 0;

    var spark = new SparkMD5.ArrayBuffer();

    file_reader.onload = function(e){
        spark.append(e.target.result);
        current_chunk++;

        if (current_chunk < chunks){
            var start = current_chunk * chunk_size, end = start + chunk_size >= file.size ? file.size : start + chunk_size;
            file_reader.readAsArrayBuffer(blob_slice.call(file, start, end));
        }else{
            var md5 = spark.end();
            $.ajax({
                url:'/speed_file.py',
                dataType: 'json',
                type: 'POST',
                data: {'md5': md5, 'file_name': file.name, 'file_key': $('#file_key').val()},
                success: function (response){
                    error = response['error'];
                    if (error){
                        alert(error);
                        return
                    }
                    show_last_upload();
                    write_manager_wrap_all({'file_key': response['file_key'],
                        'file_name': response['file_name']});
                },
                error: function(xhr, status_text){
                    __up_new_file();
                }
            });
        }

    };
    var start = current_chunk * chunk_size, end = start + chunk_size >= file.size ? file.size : start + chunk_size;
    file_reader.readAsArrayBuffer(blob_slice.call(file, start, end));
    return;
}

function __up_new_file(){
    $('#add_file_form').ajaxSubmit({
        dataType: 'json',
    beforeSend: function(){
        $('#up_process').css('width', '0%');
        $('#add_file_form').fadeOut();
    },
    uploadProgress: function(event, position, total, precentComplete){
        $('#up_process').css('width', precentComplete + '%');
    },
    error: function (xhr, status_text, t){
        alert('上传失败');
    },
    success:function (response){
        $('#up_process').fadeOut(2000);
        error = response['error'];
        if (error){
            alert(error);
            return
        }
        show_last_upload();
        write_manager_wrap_all({'file_key': response['file_key'],
            'file_name': response['file_name']});
    },
    });
}

function write_manager_wrap_all(data){
    $input_key = $('#input_key_wrap');
    if (! $input_key.find('.input_key').val().trim()){
        return;
    }
    $.ajax({url: "/manage.py", 
        dataType:'json',
    type:'POST',
    data:data,
    success:
        function (data){
            var error = data['error'];
            if (error){
                alert(error);
                return false;
            }
            $input_key.hide();

            var result = data['result'];
            $main = $('#main');
            for (i in result){
                var $wrap = $($('.manage_wrap')[0]).clone();
                var _data = result[i];
                write_manager_wrap($wrap, _data);
                $wrap.fadeIn(i * 200 + 200);
                $main.append($wrap);
            }
            $('#file_key').val($input_key.find('.input_key').val());
            $('#add_file_form').fadeIn();
            $('#main').removeClass('b_bg');
            $('body').css('background-image', "url('http://7u2ph0.com1.z0.glb.clouddn.com/images/bg_manage.jpg')");
        },});

}

function write_manager_wrap($wrap, data){
                if (!data['can_share']){ // 如果不可以共享，就不要那个按钮了
                    $wrap.find('.btn_file_share').remove();
                }
                change_share_btn($wrap, data['share_id']);
                $wrap.find('.file_name').html(data['file_name']).val(data['file_name']);
                $wrap.find('.upload_time').html(DateToString(data['upload_time']));
                $wrap.find('.expired_time').html(DateToString(data['expired_time']));
                $wrap.find('.file_size').html(data['file_size']);
                $wrap.find('.file_key').val(data['file_key']);
                $('#file_key').val(data['file_key']);

                if (data['content_type'].split('/')[0] == 'image'){
                    $wrap.find('.pci_summary').attr('src', data['file_url']);
                }
                if (data['is_vip']){
                    $wrap.addClass('vip_bg');
                }
}

