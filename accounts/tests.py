from django.test import TestCase, Client
from django.shortcuts import reverse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.timezone import now

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

class ConversionWorkflowTests(TestCase):
    def test_convert_user(self):
        c = Client()
        home_response = c.post(reverse('home'))  # visit the homepage
        expected_url = reverse('workcashflow')
        self.assertRedirects(home_response, expected_url)

        starting_savings = 42
        yearly_income = 100
        yearly_expenses = 100
        start_date = now().date()

        data = {'starting_savings': starting_savings,
                'yearly_income':yearly_income, 
                'yearly_expenses':yearly_expenses, 
                'start_date':start_date,
                'submit':'submit'}

        cashflow_response = c.post(home_response.url, data, follow=True)
        expected_url = reverse('home')
        self.assertRedirects(cashflow_response, expected_url)

        expected_content = "<a href = '/tarot/convert'><u> register </u></a>"
        self.assertContains(cashflow_response, expected_content)

        username = 'michael'
        password = 'good_enough'
        data = {'username': username, 'password1': password, 'password2':password}
        convert_response = c.post(reverse('guest_user_convert'), data)
        expected_url = reverse('home')
        self.assertRedirects(convert_response, expected_url)

        home_response = c.get(convert_response.url)
        expected_content = username
        self.assertContains(home_response, expected_content)
        expected_content = starting_savings
        self.assertContains(home_response, starting_savings)

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
