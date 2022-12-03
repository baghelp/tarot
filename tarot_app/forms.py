from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import WorkCashflow, ChangeInIncome, ChangeInExpenses, Goal, Datapoint
import datetime

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
        self.fields['starting_savings'].help_text = 'how much is in your savings to start?'
        self.fields['starting_retirement'].help_text = 'how much is in your retirement account to start?'
        self.fields['yearly_income'].help_text = 'input your income after taxes'
        self.fields['amount_kept_in_savings'].help_text = 'how much do you intend to keep in savings?'
        self.fields['added_yearly_to_retirement'].help_text = 'how much do you intend to contribute to retirement?'
        self.fields['retirement_yearly_growth_rate'].help_text = 'eg, enter \'8\' for 8% growth each year'
        self.fields['retirement_yearly_growth_rate'].label = 'Retirement yearly growth rate (%)'
        self.fields['other_investment_yearly_growth_rate'].help_text = 'eg, enter \'8\' for 8% growth each year'
        self.fields['other_investment_yearly_growth_rate'].label = 'Other investments yearly growth rate (%)'


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
        widgets = {
            'dollar_value_date': widgets.DateInput(attrs={'type': 'date'}),
            'goal_date': widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['assumed_yearly_inflation'].help_text = 'eg, enter \'3\' for 3% inflation each year'
        self.fields['dollar_value_date'].label = 'What dollar is your goal set in?'
        self.fields['dollar_value_date'].help_text = 'eg, 1970-dollars, 2022-dollars, etc'
        self.fields['goal_date'].help_text = 'when you\'d like to meet your goal'



class RecordDatapointForm(forms.ModelForm):
    
    class Meta:
        model = Datapoint
        fields = "__all__"
        exclude = ('user',)
        widgets = {
            'observed_date': widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(RecordDatapointForm, self).__init__(*args, **kwargs)

