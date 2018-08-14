import datetime
import uuid
import random
from datetime import datetime, timedelta, date
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
import dysms_python.demo_sms_send as sms

from clothes.models import *
from users.models import UserProfile, MobileVerifyRecord
from operations.models import  Banner
from users.forms import LoginForm,RegistForm,ModifyForm,ForgetPwForm,HeadImgForm,TRANS

# Create your views here.
def index(request):
    seasons = None
    user_info = None
    banner = None
    newest_clothes = None
    hotest_clothes = None
    try:
        user_info = UserProfile.objects.filter(username=request.user.username)[0]
    except:
        pass
    try:
        seasons = Season.objects.order_by('index')
        banner = Banner.objects.order_by('add_time')[:3]
        season = request.GET.get('season','all')
        if season!='all':
            tmp = Clothes.objects.filter(seasons__name=season)
        else:
            tmp = Clothes.objects
        newest_clothes =list(map(lambda x:{'colorImg':x.colors.all()[0],'colors':set(map(lambda y:y.name,x.colors.all())),'price':x.price,'c_id':x.id},tmp.order_by('update_time')[:3]))
        lastDate = tmp.latest('update_time').update_time
        lastDate = date(lastDate.year,lastDate.month,lastDate.day)
        hotest_clothes =list(map(lambda x:{'colorImg':x.colors.all()[0],'colors':set(map(lambda y:y.name,x.colors.all())),'price':x.price,'c_id':x.id},tmp.filter(update_time__range=(lastDate-timedelta(days=70),lastDate)).order_by('sold')[:3]))
    except:
        pass
    finally:
        pass

    context={'seasons':seasons,'user_info':user_info,'banner':banner,'newest_clothes':newest_clothes,'hotest_clothes':hotest_clothes,'cson':season}
    return render(request, 'index.html', context=context)


class LoginView(View):
    def get(self,request):
        return redirect('/')

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            phoneNum = request.POST.get("phoneNum")
            passWd = request.POST.get("passWd")
            user = authenticate(username = phoneNum,password = passWd)
            if user is not None:
                login(request,user)
                return HttpResponse('OK')
            else:
                return HttpResponse('用户名或密码错误')
        else:
            info = ""
            for key, error in login_form.errors.items():
                info = info+"%s : %s"%(key,error)
            return HttpResponse(info)


def user_logout(request):
    logout(request)
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if redirect_to and redirect_to!='/user/':
        return redirect(redirect_to)
    else:
        return redirect('/')


class RegistView(View):
    def get(self,request):
        return render(request, "/")
    def post(self,request):
        regist_form = RegistForm(request.POST)
        if regist_form.is_valid():
            phoneNum = request.POST.get("regPhoneNum")
            passWd = request.POST.get("regPassWd")
            verify_code = request.POST.get("verifyCode")
            try:
                record = MobileVerifyRecord.objects.filter(phone=phoneNum,send_type='register').latest('send_time')
                send_time = datetime(record.send_time.year,record.send_time.month,record.send_time.day,record.send_time.hour,record.send_time.minute,record.send_time.second)
                if send_time+timedelta(minutes=5)>datetime.now():
                    if verify_code == record.code:
                        if not UserProfile.objects.filter(mobile=phoneNum).exists():
                            UserProfile.objects.create(username=phoneNum,mobile=phoneNum,password=passWd)
                            #login and return to index
                            user = authenticate(username=phoneNum, password=passWd)
                            if user is not None:
                                login(request, user)
                                return HttpResponse('OK')
                            else:
                                return HttpResponse("用户名或密码错误")
                        else:
                            return HttpResponse("用户已存在")
                    else:
                        return HttpResponse("验证码有误")
                else:
                    return HttpResponse("验证码过期")
            except:
                return HttpResponse("系统短信服务异常")
        else:
            info = ""
            for key, error in regist_form.errors.items():
                info = info+"%s : %s"%(TRANS[key],error)
            return HttpResponse(info)


class SendVerifyCodeView(View):
    def post(self,request):
        phone = request.POST.get("acc")
        __business_id = uuid.uuid1()
        code = ''
        for i in range(6):
            code += str(random.randint(0,9))
        params = {'code':code}
        if request.POST.get("type") == 'regist':
            send_type = "register"
            state = sms.send_sms(__business_id, phone, "公司名称", "申请的sms号码", str(params))
            if json.loads(state)["Code"]=="OK":
                MobileVerifyRecord.objects.create(code=code,phone=phone,send_type=send_type)
            return HttpResponse('')
        elif request.POST.get("type") == 'forget':
            send_type = "forget"
            state = sms.send_sms(__business_id, phone, "公司名称", "申请的sms号码", str(params))
            if json.loads(state)["Code"] == "OK":
                MobileVerifyRecord.objects.create(code=code, phone=phone, send_type=send_type)
            return HttpResponse('')
        else:
            redirect_to = request.POST.get('next', request.GET.get('next', ''))
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')


class Unbound(LoginRequiredMixin,View):
    def post(self,request):
        pass


class UserCenter(LoginRequiredMixin,View):
    def get(self,request):
        user_info=None
        all_seasons = []
        _favs = []
        try:
            all_seasons = Season.objects.order_by('index').values('name')
            user_info = UserProfile.objects.filter(username=request.user.username)[0]
            favs = list(user_info.fav.values_list('id'))
            for fav in favs:
                color = Clothes.objects.get(id=fav[0]).colors.first()
                _favs.append({'name': color.clothing.name, 'brand': color.clothing.brand, 'fabric': color.clothing.fabric, 'c_id': fav[0],'color':color.id,"img":color.colorImg,'all_color':set(map(lambda x:x.name,color.clothing.colors.all()))})
        except:
            pass
        return render(request,'user.html',{'user_info':user_info,'favs':_favs,'all_seasons':all_seasons})


# Create your views here.
class UserFav(LoginRequiredMixin,View):
    def post(self,request):
        _user = UserProfile.objects.get(username=request.user.username)
        _c_id = request.POST.get('c_id', 1)
        try:
            _user.fav.add(Clothes.objects.get(id=_c_id))
        except:
            return HttpResponse('暂时无法提供服务')
        return HttpResponse('success')


class UserUnFav(LoginRequiredMixin,View):
    def post(self,request):
        _user = UserProfile.objects.get(username=request.user.username)
        _c_id = request.POST.get('c_id', 1)
        try:
            _user.fav.remove(Clothes.objects.get(id=_c_id))
        except:
            return HttpResponse('暂时无法提供服务')
        return HttpResponse('success')


class ChangeHead(LoginRequiredMixin,View):
    def post(self,request):
        img_form = HeadImgForm(request.POST, request.FILES)
        if img_form.is_valid():
            try:
                request.user.image = img_form.cleaned_data['image']
                request.user.save()
            except:
                pass
            return HttpResponse('status:OK')
        else:
            info = ""
            for key, error in img_form.errors.items():
                info = info + "%s : %s" % (TRANS[key], error)
            return HttpResponse(info)


class UserModify(LoginRequiredMixin,View):
    def post(self,request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            _user = UserProfile.objects.filter(username=request.user.username)[0]
            _user.nick_name = request.POST.get('nickName')
            _user.gender = request.POST.get('gender')
            _user.birthday = request.POST.get('birthday')
            _user.address = request.POST.get('address')
            try:
                _user.save()
            except:
                pass
            return HttpResponse('OK')
        else:
            info = ""
            for key, error in modify_form.errors.items():
                info = info + "%s : %s" % (TRANS[key], error)
            return HttpResponse(info)


class ForgetPW(View):
    def get(self,request):
        return render(request,'forgetPw.html',{})
    def post(self,request):
        reset_form = ForgetPwForm(request.POST)
        if reset_form.is_valid():
            _phone = request.POST.get('phoneNum')
            _pw = request.POST.get('passWd')
            _code = request.POST.get('verifyCode')
            try:
                record = MobileVerifyRecord.objects.filter(phone=_phone, send_type='forget').latest('send_time')
                send_time = datetime(record.send_time.year, record.send_time.month, record.send_time.day,
                                     record.send_time.hour, record.send_time.minute, record.send_time.second)
                if send_time+timedelta(minutes=15)>datetime.now():
                    if _code == record.code:
                        try:
                            _user = UserProfile.objects.filter(mobile=_phone)[0]
                            _user.password = make_password(_pw)
                            _user.save()
                            return HttpResponse('重置成功')
                        except:
                            HttpResponse('用户不存在')
                    else:
                        return HttpResponse('验证码有误')
                else:
                    return HttpResponse('验证码过期')
            except:
                return HttpResponse('短信服务异常')
        else:
            info = ""
            for key, error in reset_form.errors.items():
                info = info + "%s : %s" % (TRANS[key], error)
            return HttpResponse(info)
        return HttpResponse('短信服务异常')