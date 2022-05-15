from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from guest_user.decorators import regular_user_required
from .forms import DeleteAccountForm

def register_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect(reverse('index'))
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()
    return render (request = request, template_name = 'tarot_accounts/register.html', context = {'register_form':form})

@regular_user_required
def account_management(request):
    return render (request = request, template_name = 'tarot_accounts/account_management.html')

@regular_user_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST, username = request.user.username)
        if form.is_valid():
            u = User.objects.get(pk = request.user.pk)
            u.delete()
            # delete user, account, and associated data
            messages.success(request, 'Account Deleted.')
            return redirect(reverse('delete_account_done'))
        else:
            messages.error(request, 'Username doesn\'t match.')
    else:
        form = DeleteAccountForm()
    return render (request = request, template_name = 'tarot_accounts/delete_account_form.html', context = {'delete_account_form':form})

def delete_account_done(request):
    return render (request = request, template_name = 'tarot_accounts/delete_account_done.html')
