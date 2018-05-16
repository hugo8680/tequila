$(document).ready(function() {
    $.backstretch("/static/img/backgrounds/background.jpg");
    $('.registration-form fieldset:first-child').fadeIn('slow');
    if($('#baseMessage')) {
        setTimeout(function () {
            $('#baseMessage').remove();
            }, 1000);
    }
});
$('#signBtn').click(function () {
   if($(this).html() !== '登录') {
       $('#signOutModal').modal('show');
       $('#signOut').click(function () {
           window.location.href = '/auth/logout?next=' + getCurrentUrl();
       });
       return false;
   }else{
       window.location.href = '/auth/login?next=' + getCurrentUrl();
       return false;
   }
});

function getCurrentUrl() {
    return window.location.pathname;
}

function getQueryString(name) {
    let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    let r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(r[2]); return null;
}
