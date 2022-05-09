from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from guest_user.decorators import regular_user_required

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
