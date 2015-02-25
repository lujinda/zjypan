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
function show_err_message(error){
    $('.file_percent').css({'background-color': 'red',
        'width':'100%'});
    $('.file_percent').html(error);
}
function show_succ_message(file_key){
    $('.file_percent').css({'width': '100%','background-color': '#47CF00', 'color':'#000', 'line-height':'100%'});
    $('.file_percent').html(String.format(
                '<div class="file_key_mess">您的文件代码是:<span class="file_key">{0}</span></div><div class="file_key_tip">文件代码由日期+星期+随机两位字母组成</div>', file_key));
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
    }


