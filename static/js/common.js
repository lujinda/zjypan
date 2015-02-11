String.format = function(src){
    if (arguments.length == 0)
        return null;
    var args = Array.prototype.slice.call(arguments, 1);
    return src.replace(/\{(\d+)\}/g, function(m, i){
        return args[i];
    });
};
function DateToString(seconds){
    d = new Date(seconds * 1000);
    return d.toLocaleString();
}

function update_code_img(){
    // 防止浏览器缓存
    var url = '/code.py?token=' + $('#token').val() + '&t=' + (new Date().valueOf());
    $('#code_img').attr('src', url);
}
