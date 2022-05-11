from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from django.utils.timezone import now

class WorkCashflow(models.Model):
    starting_savings = models.IntegerField(default=0)
    yearly_income = models.IntegerField(default=70000)
    yearly_expenses = models.IntegerField(default=50000)
    start_date = models.DateField(default=now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ChangeInIncome(models.Model):
    name = models.CharField(max_length=200)
    new_yearly_income = models.IntegerField()
    start_date = models.DateField(default=now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

'''
    def clean(self):
        if self.start_date < self.cashflow.start_date:
            raise ValidationError('change in income must happen after expense and income have begun')
            '''

class ChangeInExpenses(models.Model):
    name = models.CharField(max_length=200)
    new_yearly_expenses = models.IntegerField()
    start_date = models.DateField(default=now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

'''
    def clean(self):
        if self.date < self.cashflow.date:
            raise ValidationError('change in expense must happen after expense and income have begun')
'''
    
class Goal(models.Model):
    name = models.CharField(max_length=200)
    goal_amount = models.IntegerField()
    dollar_value_date = models.DateField(default=now())
    assumed_yearly_inflation = models.IntegerField(default=3)
    goal_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    '''
        default=WorkCashflow(name='work', start_amount=0, yearly_income=0, yearly_expenses=0, start_date=datetime.today()))
    '''

    def __str__(self):
        return self.name

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
class Goal(models.Model):
    name = models.CharField(max_length=200)
    goal_amount = models.IntegerField()
    goal_date = models.DateField()
    start_amount = models.IntegerField()
    start_date = models.DateField()
    yearly_income = models.IntegerField()
    yearly_expenses = models.IntegerField()
    interest_rate = models.DecimalField(decimal_places = 2, max_digits = 3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def clean(self):
        if self.goal_date and self.start_date and self.goal_date <= self.start_date:
            raise ValidationError('goal date must be after start date')
        #TODO: figure out how to tell the user that the date was bad
        #TODO: warn about date restriction on main page
'''
