from django.contrib import admin
from .models import  WorkCashflow, ChangeInIncome, ChangeInExpenses, Goal

admin.site.register(WorkCashflow)
admin.site.register(ChangeInIncome)
admin.site.register(ChangeInExpenses)
admin.site.register(Goal)

# Register your models here.
