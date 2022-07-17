from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import UserRegistractionForm, UserEditForm, ProfileEditForm
# from .forms import LoginForm,
from django.http import HttpResponse
from .models import Profile

# Create your views here.
# Note the difference between authenticate and login:
# authenticate() checks user credentials and returns a User object if they are correct;
#  login() sets the user in the current session.

# def user_login(request):  # we use django built-in auth system so we dont need this.. just for reference
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is None:
#                 return HttpResponse('Invalid login')

#             if user.is_active:
#                 login(request, user)
#                 return HttpResponse('Authenticated successfully')
#             else:

#                 return HttpResponse('Disabled Account')
#     else:
#         form = LoginForm()

#     return render(request, 'my_app/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'my_app/dashboard.html', {'section': dashboard})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistractionForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request, 'my_app/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistractionForm()

    return render(request, 'my_app/register.html', {'user_form': user_form})


@login_required
def edit(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '
                             'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'my_app/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
