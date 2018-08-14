/*获取验证码*/
var isPhone = 1;
function getCode(e,type){
	checkPhone(); //验证手机号码
	if(isPhone){
		request_phone_code(type);//发短信
		resetCode(); //倒计时
	}else{
		$('#regisAcc').focus();
	}

}
//验证手机号码
function checkPhone(){
	var phone = $('#regisAcc').val();
	var pattern = /^1[0-9]{10}$/;
	isPhone = 1;
	if(phone == '') {
		alert('请输入手机号码');
		isPhone = 0;
		return;
	}
	if(!pattern.test(phone)){
		alert('请输入正确的手机号码');
		isPhone = 0;
		return;
	}
}
//倒计时
function resetCode(){
	$('#J_getCode').hide();
	$('#J_second').html('30');
	$('#J_resetCode').show();
	var second = 30;
	var timer = null;
	timer = setInterval(function(){
		second -= 1;
		if(second >0 ){
			$('#J_second').html(second);
		}else{
			clearInterval(timer);
			$('#J_getCode').show();
			$('#J_resetCode').hide();
		}
	},1000);
}

//发短信
function request_phone_code(type)
{
	var phone = $('#regisAcc').val();
	var data = { type:type,acc:phone };
	$.post('/send_verify_code/', data, function(result) {
		$('#regist-result').html(result);
    });

}

//获得csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});