from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import WorkCashflow, ChangeInIncome, ChangeInExpenses, Goal, OneTimeInvestment, RecurringInvestment
import datetime


class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        #fields = ("username", "email", "password1", "password2")
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

class WorkCashflowForm(forms.ModelForm):
    
    class Meta:
        model = WorkCashflow
        fields = "__all__"
        exclude = ('user',)


    def __init__(self, *args, **kwargs):
        super(WorkCashflowForm, self).__init__(*args, **kwargs)

        self.fields['name'].initial = 'starting income and expenses'
        self.fields['starting_savings'].initial = 0
        self.fields['starting_savings'].help_text = 'how much will you have to start?'
        self.fields['yearly_income'].initial = 70000
        self.fields['yearly_expenses'].initial = 50000
        self.fields['start_date'].initial = datetime.date.today()


class ChangeInIncomeForm(forms.ModelForm):
    
    class Meta:
        model = ChangeInIncome
        fields = "__all__"
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ChangeInIncomeForm, self).__init__(*args, **kwargs)

class ChangeInExpensesForm(forms.ModelForm):
    
    class Meta:
        model = ChangeInExpenses
        fields = "__all__"
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ChangeInExpensesForm, self).__init__(*args, **kwargs)

class GoalForm(forms.ModelForm):
    
    class Meta:
        model = Goal
        fields = "__all__"
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)

class OneTimeInvestmentForm(forms.ModelForm):
    
    class Meta:
        model = OneTimeInvestment
        fields = "__all__"
        exclude = ('user',)

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

    def __init__(self, *args, **kwargs):
        super(RecurringInvestmentForm, self).__init__(*args, **kwargs)

        self.fields['amount'].help_text = 'how much will you invest each time?'
        self.fields['investment_frequency'].help_text = 'how many times per year will you invest?'
        self.fields['yearly_growth'].help_text = 'eg, enter \'3\' for 3% growth each year'
        self.fields['stop_date'].help_text = 'when will you stop adding money? (optional)'
        self.fields['sell_date'].help_text = 'when will you sell this investment? (optional)'

