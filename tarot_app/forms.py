from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import WorkCashflow, ChangeInIncome, ChangeInExpenses, Goal, OneTimeInvestment, RecurringInvestment
import datetime


'''
class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit = False)
        #user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        #fields = ("username", "email", "password1", "password2")
        fields = ("username", "password")
        '''

class WorkCashflowForm(forms.ModelForm):
    
    class Meta:
        model = WorkCashflow
        fields = "__all__"
        exclude = ('user',)
        widgets = {
            'start_date': widgets.DateInput(attrs={'type': 'date'})
        }


    def __init__(self, *args, **kwargs):
        super(WorkCashflowForm, self).__init__(*args, **kwargs)
        self.fields['starting_savings'].help_text = 'how much will you have to start?'


class ChangeInIncomeForm(forms.ModelForm):
    
    class Meta:
        model = ChangeInIncome
        fields = "__all__"
        exclude = ('user',)
        widgets = {
            'start_date': widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ChangeInIncomeForm, self).__init__(*args, **kwargs)

class ChangeInExpensesForm(forms.ModelForm):
    
    class Meta:
        model = ChangeInExpenses
        fields = "__all__"
        exclude = ('user',)
        widgets = {
            'start_date': widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ChangeInExpensesForm, self).__init__(*args, **kwargs)

class GoalForm(forms.ModelForm):
    
    class Meta:
        model = Goal
        fields = "__all__"
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['assumed_yearly_inflation'].help_text = 'eg, enter \'3\' for 3% inflation each year'
        self.fields['dollar_value_date'].label = 'What dollar is your goal set in?'
        self.fields['dollar_value_date'].help_text = 'eg, 1970 dollars or 2022 dollars'
        self.fields['goal_date'].help_text = 'when you want to meet your goal'

class OneTimeInvestmentForm(forms.ModelForm):
    
    class Meta:
        model = OneTimeInvestment
        fields = "__all__"
        exclude = ('user',)
        widgets = {
            'start_date': widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(OneTimeInvestmentForm, self).__init__(*args, **kwargs)

        self.fields['amount'].help_text = 'how much will you invest?'
        self.fields['yearly_growth'].help_text = 'eg, enter \'3\' for 3% growth each year'
        self.fields['sell_date'].help_text = 'when will you sell this investment? (optional)'

class RecurringInvestmentForm(forms.ModelForm):
    
    class Meta:
        model = RecurringInvestment
        fields = "__all__"
        exclude = ('user',)
        widgets = {
            'start_date': widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(RecurringInvestmentForm, self).__init__(*args, **kwargs)

        self.fields['amount'].help_text = 'how much will you invest each time?'
        self.fields['investment_frequency'].help_text = 'how many times per year will you invest?'
        self.fields['yearly_growth'].help_text = 'eg, enter \'3\' for 3% growth each year'
        self.fields['stop_date'].help_text = 'when will you stop adding money? (optional)'
        self.fields['sell_date'].help_text = 'when will you sell this investment? (optional)'

