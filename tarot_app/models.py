from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from django.utils.timezone import now

class WorkCashflow(models.Model):
    starting_savings = models.IntegerField(default=0)
    starting_retirement = models.IntegerField(default=0)
    start_date = models.DateField(default=now())
    yearly_income = models.IntegerField(default=70000)
    yearly_expenses = models.IntegerField(default=50000)
    amount_kept_in_savings = models.IntegerField(default=10000)
    added_yearly_to_retirement = models.IntegerField(default=20000)
    retirement_yearly_growth_rate = models.IntegerField(default=8)
    other_investment_yearly_growth_rate = models.IntegerField(default=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + '\'s work_cashflow'

class ChangeInIncome(models.Model):
    name = models.CharField(max_length=200)
    new_yearly_income = models.IntegerField()
    start_date = models.DateField(default=now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ChangeInExpenses(models.Model):
    name = models.CharField(max_length=200)
    new_yearly_expenses = models.IntegerField()
    start_date = models.DateField(default=now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class Goal(models.Model):
    name = models.CharField(max_length=200)
    goal_amount = models.IntegerField()
    dollar_value_date = models.DateField(default=now())
    assumed_yearly_inflation = models.IntegerField(default=3)
    goal_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

'''
class OneTimeInvestment(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    yearly_growth = models.DecimalField(decimal_places = 2, max_digits = 6)
    start_date = models.DateField(default=now())
    sell_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class RecurringInvestment(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField(default=now())
    amount = models.IntegerField()
    investment_frequency = models.IntegerField() #TODO: times per year
    yearly_growth = models.DecimalField(decimal_places = 2, max_digits = 6)
    stop_date = models.DateField(blank=True, null=True)
    sell_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
'''
