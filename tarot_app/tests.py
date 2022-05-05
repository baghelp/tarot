from django.test import TestCase, Client
from django.shortcuts import reverse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import pdb
#from HttpRequest import request

class RegistrationTests(TestCase):
    def test_create_user_with_valid_form_entry(self):
        username = 'valid'
        password = 'Sifre.50'
        c = Client()
        data = {'username': username, 'password1': password, 'password2':password}
        response = c.post(reverse('register'), data)
        expected_url = (reverse('index'))
        self.assertRedirects(response, expected_url)

    def test_create_user_with_invalid_form_entry(self):
        username = 'invalid'
        password = 'test'
        c = Client()
        data =  {'username': username, 'password1': password, 'password2':password}
        response = c.post(reverse('register'), data)
        expected_content = 'This password is too short'
        self.assertContains(response, expected_content)

    def test_create_duplicate_user(self):
        username = 'invalid'
        password = 'Sifre.50'
        c = Client()
        data =  {'username': username, 'password1': password, 'password2':password}
        c.post(reverse('register'), data)  # make this user
        response = c.post(reverse('register'), data)  # try to make again
        expected_content = 'user with that username already exists'
        self.assertContains(response, expected_content)


class LoginTests(TestCase):
    def test_login_user_with_valid_form_entry(self):
        username = 'michael'
        password = 'yep'
        user = User.objects.create_user(username = username, password = password)
        c = Client()
        data = {'username': username, 'password': password}
        response = c.post(reverse('login'), data, follow=True)
        expected_url = reverse('workcashflow')
        self.assertRedirects(response, expected_url)

    def test_login_user_with_invalid_form_entry(self):
        username = 'michael'
        password = 'nope'
        c = Client()
        data = {'username': username, 'password': password}
        response = c.post(reverse('login'), data)
        expected_content = 'Please enter a correct username'
        self.assertContains(response, expected_content)


# Create your tests here.
