let lastQid;
$(document).ready(function () {
    loadQuestion(0);
});

$('#nextQuestions').click(function () {
    loadQuestion(0, lastQid);
});

$('#preQuestions').click(function () {
    loadQuestion(1, lastQid);
});

function loadQuestion(pre, last_qid) {
    $.ajax({
        url: '/question/list',
        type: 'get',
        data: {
            pre: pre,
            lqid: last_qid
        },
        dataType: 'json',
        success: function (res) {
            if (res.status === 200 && res.data) {
                let data = res.data.question_list;
                if(data.length) {
                    let h = "";
                    for (let i in data) {
                        h += "<a style='text-align: left' class='list-group-item' href='/question/detail/" + data[i].qid + "'>" +
                            "<span>" + data[i].abstract + "</span>" +
                            "<span style='float: right;margin-right: 25px' class='glyphicon glyphicon-pencil'> " + data[i].answer_count + "</span>" +
                            "<span style='float: right;margin-right: 25px' class='glyphicon glyphicon-eye-open'> " + data[i].view_count + "</span>" +
                            "<span style='float: right;margin-right: 25px' class='glyphicon glyphicon-user'> " + data[i].username + "</span>" +
                            "</a>"
                    }
                    $('#question-list').html(h);
                    lastQid = res.data.last_qid;
                }else {
                    $('#question-list').prepend("<div id='pageMessage' class='alert alert-danger'>没有更多了</div>");
                    setTimeout(function () {
                        $('#question-list').find('#pageMessage').remove();
                    }, 1000);
                }
            }
        }
    })
}