from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterationForm
from .models import Account, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from django.db.models import Q
from core.models import Post,  FriendRequest

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .tasks import email_send_task, ForgotPassword_send_task

# Create your views here.




def register(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # user activation
            domain = get_current_site(request)
            email_send_task.delay(
                user.id, email, get_current_site(request).domain)

            return redirect('/accounts/register/?command=verification&email='+email)

    else:
        form = RegisterationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        users = authenticate(email=email, password=password)
        print('user:', users)

        if users is not None:
            login(request, users)
            return redirect('feed')

        else:
            messages.error(request, 'Please! Enter correct email and password')
            return redirect('login')
    return render(request, 'accounts/register.html')


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    return HttpResponse('Ok')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # user activation

            domain = get_current_site(request)
            ForgotPassword_send_task.delay(
                user.id, email, get_current_site(request).domain)

            messages.success(
                request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def reset_password_validate(request,  uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')



@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(active=True, user=request.user).order_by("-id")

    context = {
        "profile": profile,
        "posts" : posts,
    }

    return render(request, "accounts/my-profile.html", context)


@login_required
def friend_profile(request, username):
    profile = Profile.objects.get(user__username=username)
    if request.user.profile == profile:
        return redirect("my-profile")
    
    posts = Post.objects.filter(active=True, user=profile.user).order_by("-id")

    # Send Friend Request Feature
    bool = False
    bool_friend = False

    sender = request.user
    receiver = profile.user
    bool_friend = False
    print("========================  Add or cancel")
    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
        if friend_request:
            bool = True
        else:
            bool = False
    except:
        bool = False
    print("Bool =======================", bool)
    

    context = {
        "posts":posts,
        "bool_friend":bool_friend,
        "bool":bool,
        "profile":profile,
    }
    return render(request, "accounts/friend-profile.html", context)


# @login_required
# def profile_update(request):
#     if request.method == "POST":
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         u_form = UserUpdateForm(request.POST, instance=request.user)

#         if p_form.is_valid() and u_form.is_valid():
#             p_form.save()
#             u_form.save()
#             messages.success(request, "Profile Updated Successfully.")
#             return redirect('userauths:profile-update')
#     else:
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#         u_form = UserUpdateForm(instance=request.user)

#     context = {
#         'p_form': p_form,
#         'u_form': u_form,
#     }
#     return render(request, '
# accounts/profile-update.html', context)



# Inbox Functionality
