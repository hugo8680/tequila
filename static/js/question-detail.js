$(document).ready(function () {
    if($('#signBtn').html() !== '登录') {
        editorRefresh();
    }else{
        $('#answer-textarea').val('您必须登录才能回答该问题');
        $('#submit-answer').attr('disabled', 'disabled');
        $('#answer-textarea').attr('readonly', 'readonly');
    }
    loadAnswers();
});

function editorRefresh() {
    new Simditor({
        textarea: $('#answer-textarea'),
        placeholder: '请输入18-5000字的答案...',
        toolbarFloat: true,
        toolbarFloatOffset: 0,
        pasteImage: true,//允许粘贴图片
        toolbarHidden: false,
        locale: 'zh-CN',
        toolbar: [
            'bold',
            'italic',
            'underline',
            'strikethrough',
            'fontScale',
            'color',
            'ol',
            'ul',
            'code',
            'image',
            'blockquote',
            'table',
            'link',
            'hr'],
        upload: {
            url: '/question/picload', //文件上传的接口地址
            params: null, //键值对,指定文件上传接口的额外参数,上传的时候随文件一起提交
            fileKey: 'pic', //服务器端获取文件数据的参数名
            connectionCount: 3,
            leaveConfirm: '正在上传文件...'
        }
    });
}

$('#submit-answer').click(function () {
    let content = $('#answer-textarea').val();
    if(!content.match('^[\\s\\S]{18,5000}$')){
        $('#answer-editor').prepend("<div id='characterErr' style='margin-top: 10px' class='alert alert-danger'>字符数量不符合要求</div>");
        return false;
    }else {
        $('#characterErr').remove();
    }
    $.ajax({
        url: '/answer/create',
        type: 'post',
        data: {
            content: content,
            qid: getCurrentQid()
        },
        dataType: 'json',
        success: function (res) {
            if(res.status === 200 && res.data) {
                editorRefresh();
                loadAnswers();
            }else if(res.status === 200001) {
                $('#answer-editor').prepend("<div style='margin-top: 10px' class='alert alert-danger'>"+ res.message +"</div>");
            }else if(res.status === 200002 ) {
                $('#answer-editor').prepend("<div style='margin-top: 10px' class='alert alert-danger'>答案创建失败！</div>");
            }else if(res.status === 100006) {
                $('#answer-editor').prepend("<div style='margin-top: 10px' class='alert alert-danger'>"+ res.message +"</div>");
            }
        }
    });
    return false;
});

function loadAnswers() {
    $('#answer-list .list-group').html('');
    $.ajax({
        url: '/answer/list/' + getCurrentQid(),
        type: 'get',
        data: {},
        dataType: 'json',
        success: function (res) {
            if(res.status === 200 && res.data) {
                let answers = res.data.answer_list;
                if(answers.length) {
                    $('#notAnswer').remove();
                    let strHTML = "";
                    for(let i in answers) {
                        if(answers[i].status) {
                            strHTML += "<p><b style='font-size: 16px;color: deeppink'>"+ answers[i].username + "</b> <small>" + answers[i].created_at + "</small></p>";
                            strHTML += "<div style='background-color: lightblue' class='well well-sm list-group-item'>\n";
                            strHTML += "<p class='glyphicon glyphicon-ok' style='font-size: 16px;color: red'> 已采纳</p>\n";
                            strHTML += answers[i].content;
                            strHTML += "</div>";
                        }
                    }
                    for(let i in answers) {
                        if(!answers[i].status) {
                            strHTML += "<p><b style='font-size: 16px;color: deeppink'>"+ answers[i].username + "</b> <small>" + answers[i].created_at + "</small></p>";
                            strHTML += "<div class='well well-sm list-group-item'>\n";
                            strHTML += answers[i].content;
                            strHTML += "</div>";
                        }
                    }
                    $('#answer-list .list-group').append(strHTML);
                }else{
                    let strHTML = "<div id='notAnswer' class='alert alert-danger'>暂无回答</div>";
                    $('#answer-list .list-group').append(strHTML);
                }
            }
        }
    })
}

function getCurrentQid() {
    let pathname = window.location.pathname;
    return pathname.match('\\d{6}$')[0];
}