let loginSign;

$(document).ready(function () {
   refreshLoginVcode();
});

$('#loginVcode').click(function () {
    refreshLoginVcode();
});

$('#submitSignup').click(function () {
    let username = $('#form-username').val();
    let password = $('#form-password').val();
    let vcode = $('#form-vcode').val();
    if(!username.match('^\\w{4,12}$')) {
        $('#form-username').css('border', 'solid red');
        $('#form-username').val('');
        $('#form-username').attr('placeholder', '用户名长度应该在4-12位之间');
        return false;
    }else {
        $('#form-username').css('border', '');
    }
    if(!password.match('^\\w{6,20}$')) {
        $('#form-password').css('border', 'solid red');
        $('#form-password').val('');
        $('#form-password').attr('placeholder', '密码长度应该在6-20位之间');
        return false;
    }else {
        $('#form-password').css('border', '');
    }
    if(!vcode.match('^\\w{4}$')) {
        $('#form-vcode').css('border', 'solid red');
        $('#form-vcode').val('');
        $('#form-vcode').attr('placeholder', '验证码长度为4位');
        return false;
    }else {
        $('#form-vcode').css('border', '');
    }
    $.ajax({
        url: '/auth/signup',
        type: 'post',
        data: {
            username: username,
            password: password,
            vcode: vcode,
            sign: loginSign
        },
        dataType: 'json',
        success: function (res) {
            if(res.status === 200 && res.data) {
                window.location.href = getQueryString('next') || '/' + encodeURI('?m=登录成功&e=success');
            }else if(res.status === 100001) {
                $('#form-vcode').css('border', 'solid red');
                $('#form-vcode').val('');
                $('#form-vcode').attr('placeholder', res.message);
            }else if(res.status === 100004) {
                $('#form-username').css('border', 'solid red');
                $('#form-username').val('')
                $('#form-username').attr('placeholder', res.message);
            }else if(res.status === 100005) {
                $('.registration-form').prepend("<div id='regMessage' class='alert alert-danger'>注册失败</div>");
                setTimeout(function () {
                    $('.registration-form').find('#regMessage').remove();
                    }, 1500);
            }
        }
    })
});

$('#submitLogin').click(function () {
    let username = $('#form-username').val();
    let password = $('#form-password').val();
    let vcode = $('#form-vcode').val();
    if(!username.match('^\\w{4,12}$')) {
        $('#form-username').css('border', 'solid red');
        $('#form-username').val('');
        $('#form-username').attr('placeholder', '用户名长度应该在4-12位之间');
        return false;
    }else {
        $('#form-username').css('border', '');
    }
    if(!password.match('^\\w{6,20}$')) {
        $('#form-password').css('border', 'solid red');
        $('#form-password').val('');
        $('#form-password').attr('placeholder', '密码长度应该在6-20位之间');
        return false;
    }else {
        $('#form-password').css('border', '');
    }
    if(!vcode.match('^\\w{4}$')) {
        $('#form-vcode').css('border', 'solid red');
        $('#form-vcode').val('');
        $('#form-vcode').attr('placeholder', '验证码长度为4位');
        return false;
    }else {
        $('#form-vcode').css('border', '');
    }
    $.ajax({
        url: '/auth/login',
        type: 'post',
        data: {
            username: username,
            password: password,
            vcode: vcode,
            sign: loginSign,
        },
        dataType: 'json',
        success: function (res) {
            if(res.status === 200 && res.data) {
                window.location.href = getQueryString('next') || '/' + encodeURI('?m=登录成功&e=success');
            }else if(res.status === 100001) {
                $('#form-vcode').css('border', 'solid red');
                $('#form-vcode').val('');
                $('#form-vcode').attr('placeholder', res.message);
            }else if(res.status === 100002) {
                $('#form-username').css('border', 'solid red');
                $('#form-username').val('')
                $('#form-username').attr('placeholder', res.message);
            }else if(res.status === 100003) {
                $('#form-password').css('border', 'solid red');
                $('#form-password').val('');
                $('#form-password').attr('placeholder', res.message);
            }
        }
    })
});

function refreshLoginVcode() {
    $.ajax({
        url: '/auth/v.img',
        type: 'get',
        data: {},
        dataType: 'json',
        success: function (res) {
            if(res.status === 200 && res.data) {
                $('#loginVcode').attr('src', "data:image/png;base64," + res.data.vcode);
                loginSign = res.data.sign;
            }
        }
    })
}