# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.views.generic import View

from users.models import UserProfile,EmailVerifyRecord,Banner
from users.forms import LoginForm,RegisterForm,ForgetForm,ModifyForm,UploadImageForm,UserInfoForm
from organization.models import CourseOrg,Teacher
from operation.models import UserCourse,UserFavorite,UserMessage
from courses.models import Course

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


"""用户登录"""
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg":"用户未激活！"})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误！"})
        else:
            return render(request,'login.html',{'login_form':login_form})

"""激活账号"""
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                user=UserProfile.objects.get(email=email)
                user.is_active=True
                user.save()
        else:
            return render(request,'active_fail.html')

        return render(request,'login.html')

"""注册账号"""
class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已经存在'})
            pass_word = request.POST.get("password", "")
            user_profile=UserProfile()
            user_profile.username=user_name
            user_profile.email=user_name
            user_profile.password=make_password(pass_word)
            user_profile.is_active=False
            user_profile.save()

            send_register_email(user_name,'register')
            return render(request, "login.html")
        else:
            return render(request, "register.html",{'register_form':register_form})

"""忘记密码发链接"""
class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form=ForgetForm(request.POST)
        if forget_form.is_valid():
            email=request.POST.get('email','')
            """发送邮件"""
            send_register_email(email,'forget')
            return render(request,'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

"""转到密码重置页"""
class ResetView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email=record.email
                return render(request,'password_reset.html',{'email':email})

        else:
            return render(request,'active_fail.html')

        return render(request,'login.html')

"""新密码提交"""
class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self,request):
        modify_form=ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1','')
            pwd2=request.POST.get('password2','')
            """知道是哪个邮箱"""
            email=request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':"密码不一致"})
            user=UserProfile.objects.get(email=email)
            user.password=make_password(pwd2)
            user.save()

            return render(request,'login.html')
        else:
            email=request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modify_form':modify_form})

"""退出登录"""
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

class UserInfoView(LoginRequiredMixin,View):
    """
    用户信息
    """
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors),content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    """
    用户修改头像
    """
    def post(self,request):
        image_form=UploadImageForm(request.POST,request.FILES)
        if image_form.is_valid():
            image=image_form.cleaned_data['image']
            request.user.image=image
            request.user.save()
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail'}",content_type='application/json')



#或者如下代码与上述代码效果相同
#image_form=UploadImageForm(request.POST,request.FILES，instance=request.user)
# if image_form.is_valid():
#   image_form.save()
#   pass

class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self,request):
        modify_form=ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1=request.POST.get('password1','')
            pwd2=request.POST.get('password2','')

            if pwd1 != pwd2:
                return HttpResponse("{'status':'fail','msg':'密码不一致'}",content_type='application/json')
            user=request.user
            user.password=make_password(pwd2)
            user.save()

            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    """
    发送修改邮箱验证码
    """
    def get(self,request):
        email=request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'msg':'邮箱已存在'}",content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse("{'status':'success'}",content_type='application/json')


class UpdateEmailView(View):
    """
    修改邮箱
    """
    def post(self,request):
        email=request.POST.get('email','')
        code=request.POST.get('code','')

        existed_records=EmailVerifyRecord.objects.filter(email=email,code=code)
        if existed_records:
            user=request.user
            user.email=email
            user.save()
            return HttpResponse("{'status':'success'}",content_type='application/json')
        else:
            return HttpResponse("{'msg':'验证码出错'}",content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    """
    我的课程
    """
    def get(self,request):
        user_courses=UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses

        })


class MyFavOrgView(LoginRequiredMixin,View):
    """
    我收藏的课程
    """
    def get(self,request):
        org_list=[]
        fav_orgs=UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id=fav_org.fav_id
            org=CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list

        })


class MyFavTeacherView(LoginRequiredMixin,View):
    """
    我收藏的讲师
    """
    def get(self,request):
        teacher_list=[]
        fav_teachers=UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id=fav_teacher.fav_id
            teacher=Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list

        })


class MyFavCourseView(LoginRequiredMixin,View):
    """
    我收藏的课程
    """
    def get(self,request):
        course_list=[]
        fav_courses=UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id=fav_course.fav_id
            course=Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request,'usercenter-fav-course.html',{
            'course_list':course_list

        })


class MyMessageView(LoginRequiredMixin,View):
    """
    我的消息
    """
    def get(self,request):
        all_messages=UserMessage.objects.filter(user=request.user.id)

        """用户进入个人消息后，清空未读消息记录"""
        all_unread_messages=UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read=True
            unread_message.save()

        """对个人消息进行分页"""
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

    # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_messages,5, request=request)

        messages = p.page(page)

        return render(request,'usercenter-message.html',{
            'messages':messages
        })


class IndexView(View):
    """首页"""
    def get(self,request):
        """取出轮播图"""
        all_banners=Banner.objects.all().order_by('-index')
        courses=Course.objects.filter(is_banner=False)[:6]
        banner_courses=Course.objects.filter(is_banner=False)[:3]
        course_orgs=CourseOrg.objects.all()[:15]

        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })


#全局404页面配置
def page_not_found(request):
    from  django.shortcuts import render_to_response
    response=render_to_response('404.html',{})
    response.status_code=404
    return response


#全局500页面配置
def page_error(request):
    from  django.shortcuts import render_to_response
    response=render_to_response('500.html',{})
    response.status_code=500
    return response









