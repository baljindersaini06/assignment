from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login, authenticate,logout
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from myapp.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from .forms import SignUpForm, SetPasswordForm, PasswordChangedForm, UserForm, UserChangedForm
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic import ListView, TemplateView




# Create your views here.


def loginView(request):
    return render(request, 'registration/login.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.phone_no = form.cleaned_data.get('phone_no')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
          
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:      
        form = SignUpForm()
        
    return render(request, 'registration/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('setpassword',args=(uid,)))
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def setpassword(request,uid):
    if request.method=='POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=uid)
            password = request.POST.get('password')
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = SetPasswordForm()

    return render(request,"passwordset.html",{'form':form})

@login_required
def change_password(request):
    #print("helloooooo")
    if request.method == 'POST':
        form = PasswordChangedForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangedForm(request.user)
    return render(request, 'myapp/password.html', {'form': form})


class Disc(TemplateView):
    template_name='myapp/profile.html'


@login_required
def edit_names(request):
    args = {}
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserForm(instance=request.user)
        args['form'] = form
        return render(request, 'registration/edit_user_name.html', args)


@login_required
def update_profile(request):
    args = {}

    if request.method == 'POST':
        form = UserChangedForm(request.POST, request.FILES, instance=request.user)
        form.actual_user = request.user
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserChangedForm()

    args['form'] = form
    return render(request, 'registration/update_profile.html', args)

class Dis(TemplateView):
    template_name='myapp/profileview.html'
