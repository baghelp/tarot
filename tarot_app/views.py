from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import NewUserForm, LoginForm, WorkCashflowForm, ChangeInIncomeForm, ChangeInExpensesForm, OneTimeInvestmentForm, RecurringInvestmentForm, GoalForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, backends
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import WorkCashflow, ChangeInIncome, ChangeInExpenses, OneTimeInvestment, RecurringInvestment, Goal
from django.core import serializers
from django.forms.models import model_to_dict
from plotly.offline import plot
from datetime import timedelta
from guest_user.decorators import allow_guest_user
import math
import plotly.graph_objs as go
import json
import numpy as np

def index(request):
    return render(request = request, template_name = 'retire/index.html')

def register_request(request):
    #TODO: use this format (if, else with POST method) for the other requests as well
    if request.method == 'POST':
        #form = NewUserForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect(reverse('index'))
    #form = NewUserForm()
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
            return redirect(reverse('register'))
    form = UserCreationForm()
    return render (request = request, template_name = 'retire/register.html', context = {'register_form':form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username = data['username'], password = data['password'])
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect(reverse('home'))
        else:
            messages.error(request, form.errors)
            return redirect(reverse('login'))
    form = LoginForm()
    return render (request = request, template_name = 'retire/login.html', context = {'login_form':form})

@allow_guest_user
def home(request):
    if not request.user.workcashflow_set.exists():
        return redirect(reverse('workcashflow'))

    savings_plot = makeSavingsPlot(request, default_num_date_buckets=150)
    plot_div = [savings_plot]

    work_cashflow = request.user.workcashflow_set.all()
    changes_in_income = request.user.changeinincome_set.all()
    changes_in_expenses = request.user.changeinexpenses_set.all()
    one_time_investments = request.user.onetimeinvestment_set.all()
    recurring_investments = request.user.recurringinvestment_set.all()
    goals = request.user.goal_set.all()

    sorted_changes_in_income = sorted(changes_in_income, key = lambda x:x.start_date)
    sorted_changes_in_expenses = sorted(changes_in_expenses, key = lambda x:x.start_date)
    sorted_one_time_investments = sorted(one_time_investments, key = lambda x:x.start_date)
    sorted_recurring_investments = sorted(recurring_investments, key = lambda x:x.start_date)
    sorted_goals = goals #sorted(goals, key = lambda x:x.goal_date)# TODO: not sorted at all

    context_to_pass = {
        "plot_div":plot_div,
        "work_cashflow":work_cashflow,
        "sorted_changes_in_income":sorted_changes_in_income,
        "sorted_changes_in_expenses":sorted_changes_in_expenses,
        "sorted_one_time_investments":sorted_one_time_investments,
        "sorted_recurring_investments":sorted_recurring_investments,
        "sorted_goals":sorted_goals,
    }

    return render(request = request, template_name = 'retire/home.html', context = context_to_pass)

@allow_guest_user
def workcashflow(request):#, id=None):

    '''
    if id:
        instance = get_object_or_404( WorkCashflow, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
    '''
    existing_work_cashflows = request.user.workcashflow_set.all()
    if existing_work_cashflows:
        instance = existing_work_cashflows[0]
        can_delete = True

    else:
        can_delete = False
        instance = WorkCashflow(user = request.user)

    form = WorkCashflowForm(request.POST or None, instance = instance)

    if can_delete and request.POST.get('delete'):
        instance.delete()
        # delete was successful, redirect
        return redirect(reverse('home'))

    elif request.POST and form.is_valid(): # only save if POST. Otherwise they want to _see_ something, not _submit_ something
        form.save()

        # save was successful, redirect
        return redirect(reverse('home'))
    return render(request = request, template_name = 'retire/income_and_spending.html', context = {'workcashflow_form':form, 'can_delete':can_delete})

@allow_guest_user
def changeinincome(request, id=None):
    if id:
        instance = get_object_or_404( ChangeInIncome, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False
        instance = ChangeInIncome(user = request.user)

    form = ChangeInIncomeForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        # delete was successful, redirect
        return redirect(reverse('home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('home'))

    return render(request = request, template_name = 'retire/change_in_income.html', context = {'changeinincome_form':form, 'can_delete':can_delete})

@allow_guest_user
def changeinexpenses(request, id=None):
    if id:
        instance = get_object_or_404( ChangeInExpenses, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False
        instance = ChangeInExpenses(user = request.user)

    form = ChangeInExpensesForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        return redirect(reverse('home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('home'))

    return render(request = request, template_name = 'retire/change_in_expenses.html', context = {'changeinexpenses_form':form, 'can_delete':can_delete})

@allow_guest_user
def onetimeinvestment(request, id=None):
    if id:
        instance = get_object_or_404( OneTimeInvestment, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False
        instance = OneTimeInvestment(user = request.user)

    form = OneTimeInvestmentForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        # delete was successful, redirect
        return redirect(reverse('home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('home'))

    return render(request = request, template_name = 'retire/one_time_investment.html', context = {'onetimeinvestment_form':form, 'can_delete':can_delete})

@allow_guest_user
def recurringinvestment(request, id=None):
    if id:
        instance = get_object_or_404( RecurringInvestment, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False
        instance = RecurringInvestment(user = request.user)

    form = RecurringInvestmentForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        # delete was successful, redirect
        return redirect(reverse('home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('home'))

    return render(request = request, template_name = 'retire/recurring_investment.html', context = {'recurringinvestment_form':form, 'can_delete':can_delete})

@allow_guest_user
def goal(request, id=None):
    if id:
        instance = get_object_or_404( Goal, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False
        instance = Goal(user = request.user)

    form = GoalForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        # delete was successful, redirect
        return redirect(reverse('home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('home'))

    return render(request = request, template_name = 'retire/goal.html', context = {'goal_form':form, 'can_delete':can_delete})

def calculateDateArray(work_cashflow, goals, sorted_recurring_investments, sorted_one_time_investments, sorted_changes_in_income, sorted_changes_in_expenses, default_num_date_buckets):

    # we don't plot any data before a work_cashflow, or investment of some kind starts

    num_date_buckets = default_num_date_buckets  # initialize to reasonable value
    start_date = min([item.start_date for item in [work_cashflow] or recurring_investments or one_time_investments])

    # if there is a goal, we show make the final date the furthest-out goal date
    if goals and any([goal.goal_date for goal in goals]):
        goal_date = max([goal.goal_date for goal in goals]) + timedelta(days=30*3)  # if they have a goal, we also show 3 months after the goal
    else:
        goal_date = start_date + timedelta(days=365*10)

    date_range = goal_date - start_date
    delta_length_days = 1
    date_delta = timedelta(days = delta_length_days) # we calculate money for every single day
    num_steps_in_date_array = math.ceil(date_range / date_delta)
    date_array = [start_date + date_delta*step for step in range(num_steps_in_date_array) if start_date + date_delta*step <= goal_date ]

    date_axis_start = start_date - 30*date_delta
    date_axis_end = goal_date + 30*date_delta

    return date_array, date_delta, delta_length_days, num_steps_in_date_array, date_axis_start, date_axis_end

def makeSavingsPlot(request, default_num_date_buckets):
    work_cashflow = request.user.workcashflow_set.first()
    changes_in_income = list(request.user.changeinincome_set.all())
    changes_in_expenses = list(request.user.changeinexpenses_set.all())
    one_time_investments = list(request.user.onetimeinvestment_set.all())
    recurring_investments = list(request.user.recurringinvestment_set.all())
    goals = list(request.user.goal_set.all())

    # sort the arrays #TODO: we can probably store these arrays sorted instead of resorting every time
    sorted_changes_in_income = sorted(changes_in_income, key = lambda x:x.start_date)
    sorted_changes_in_expenses = sorted(changes_in_expenses, key = lambda x:x.start_date)
    sorted_one_time_investments = sorted(one_time_investments, key = lambda x:x.start_date)
    sorted_recurring_investments = sorted(recurring_investments, key = lambda x:x.start_date)


    date_array, date_delta, delta_length_days, num_steps_in_date_array, date_axis_start, date_axis_end = calculateDateArray( work_cashflow, goals, sorted_recurring_investments, sorted_one_time_investments, sorted_changes_in_income, sorted_changes_in_expenses, default_num_date_buckets)
    #if not changes_in_income or changes_in_expenses or one_time_investments or recurring_investments:


    # assuming that work_cashflow directly contributes to savings, calculate the savings at each day
    starting_savings = work_cashflow.starting_savings
    net_income_changes = [item for item in (changes_in_income + changes_in_expenses)]
    sorted_net_income_changes = sorted(net_income_changes, key = lambda x:x.start_date)
    net_income_change_d = {}

    #fill first element of dict
    normalized_income = work_cashflow.yearly_income * delta_length_days / 365
    normalized_expenses = work_cashflow.yearly_expenses * delta_length_days / 365

    normalized_net_income_d = {}
    normalized_net_income_d[work_cashflow.start_date] = normalized_income - normalized_expenses
    for item in sorted_net_income_changes:
        if isinstance(item, ChangeInIncome):
            normalized_income = item.new_yearly_income * delta_length_days / 365
        elif isinstance(item, ChangeInExpenses):
            normalized_expenses = item.new_yearly_expenses * delta_length_days / 365
        else:
            raise TypeError('The sorted_net_income_changes array should be made of exclusively income or expenses')
        normalized_net_income_d[item.start_date] = normalized_income - normalized_expenses
    normalized_net_income_d[date_array[-1]] = 0  # bookend signals the end of calculations

    savings_array = [starting_savings]
    for index, key in enumerate(normalized_net_income_d.keys()):
        this_date = key
        if index > 0:
            num_steps = math.ceil( (this_date - prev_date) / timedelta(days = 1) )
            savings_array += [savings_array[-1] + normalized_net_income*step for step in range(num_steps)]
        normalized_net_income = normalized_net_income_d[key]
        prev_date = this_date

    one_time_investment_values = []
    for index, item in enumerate(sorted_one_time_investments):
        start_index = np.searchsorted(date_array, item.start_date)
        savings_array[start_index+1:] = [val - item.amount for val in savings_array[start_index+1:]]

        if item.sell_date:
            end_date = item.sell_date
        else:
            end_date = date_array[-1]
        num_steps = int( (end_date - item.start_date) / timedelta(days = 1) )
        num_zeros = int( (item.start_date-date_array[0]) / timedelta(days = 1) ) + 1


        daily_growth_rate = (1+float(item.yearly_growth)/100)**(1/365)

        one_time_investment_values.append( [0]*num_zeros + [item.amount* (daily_growth_rate**step) for step in range(num_steps)] )

    recurring_investment_values = []
    for index, item in enumerate(sorted_recurring_investments):
        start_index = np.searchsorted(date_array, item.start_date)

        if item.sell_date and item.stop_date:
            end_date = min( item.sell_date, item.stop_date )
        elif item.sell_date:
            end_date = item.sell_date
        elif item.stop_date:
            end_date = item.stop_date
        else:
            end_date = date_array[-1]

        num_steps = int((end_date - item.start_date) / timedelta(days = 1))
        num_zeros = int( (item.start_date-date_array[0]) / timedelta(days = 1) ) + 1

        daily_growth_rate = (1+float(item.yearly_growth)/100)**(1/365)
        investment_array = [0]*num_zeros

        days_per_investment_period = math.ceil(365 / item.investment_frequency)
        for investment_period in range(math.ceil(num_steps / days_per_investment_period)):
            savings_array[start_index+1:] = [val - item.amount for val in savings_array[start_index+1:]]
            investment_array.append( investment_array[-1] + item.amount)

            for day in range(days_per_investment_period-1):
                if len(investment_array) < num_zeros + num_steps:
                    investment_array.append(investment_array[-1]*daily_growth_rate)
                else:
                    break
            start_index = start_index + days_per_investment_period

        recurring_investment_values.append(investment_array)

    #savings_array = [starting_savings + normalized_net_income*step for step in range(num_steps_in_date_array)]

    # TODO: possibly handle reinvesting of dividends / interest ?
    
    #interest calculation -- use for investments
    '''
    normalized_interest_rate = float(1 + goal.interest_rate)**(delta_days/365) - 1 # based on https://calculate.onl/convert-annual-interest-rates/, and verified in calculation

    # use closed-form-solution to geometric series to speed up this calculation
    P = start_money  # principal
    a = normalized_net_income  # coefficient in geometric series
    r = 1+normalized_interest_rate  # the common ratio in geometric series

    money_values = [ P*(r**n) + a*( (1 - r**n) / (1 - r) ) for n in range(len(date_values))]

    # this calculation is just for reference. The above is equivalent. see https://en.wikipedia.org/wiki/Geometric_series if you need to rederive it
    #money_values = [start_money]
    #for step in range(len(date_values) - 1):
        #money_values.append(money_values[-1]*(1+normalized_interest_rate) + normalized_net_income)
    '''

    #net_worth_array = np.sum([savings_array] + one_time_investment_values + recurring_investment_values)
    arr = np.array( [savings_array])
    for item in one_time_investment_values:
        arr = np.append(arr, [item], axis=0)
    for item in recurring_investment_values:
        arr = np.append(arr, [item], axis=0)
    net_worth_array = list(arr.sum(axis = 0))

    net_worth = go.Scatter(x = date_array, 
                      y = net_worth_array,
                      mode = 'lines', 
                      name = 'net worth',
                      opacity = 0.8, 
                      marker_color = 'green')

    savings = go.Scatter(x = date_array, 
                      y = savings_array,
                      mode = 'lines', 
                      name = 'savings',
                      opacity = 0.8)

    layout = go.Layout( paper_bgcolor='#fbfbfb',
                        plot_bgcolor='#DDDDDD',
                        #margin = go.layout.Margin( l=0, r=0, t=0, b=0),
                        margin = go.layout.Margin( t=0),
                        )

    layout.yaxis.gridcolor = 'black'
    layout.xaxis.gridcolor = 'black'
    layout.xaxis.range = [date_axis_start, date_axis_end]
    layout.title.x = 0.5
    data = [net_worth, savings]
    #data = [net_worth]
    for i, item in enumerate(one_time_investment_values):
        data.append( go.Scatter(x = date_array,
                                y = item,
                                mode = 'lines',
                                name = 'investment: ' + sorted_one_time_investments[i].name,
                                opacity = 0.8)
        )
      

    for i, item in enumerate(recurring_investment_values):
        data.append( go.Scatter(x = date_array,
                                y = item,
                                mode = 'lines',
                                name = sorted_recurring_investments[i].name,
                                opacity = 0.8)
        )

    plot_div = plot({"data": data,
                    "layout": layout},
                    output_type = 'div',
                    include_plotlyjs=False)

    return plot_div


@allow_guest_user
def new_goal(request):
    form = GoalForm(request.POST)
    if form.is_valid():
        new_goal = form.save(commit = False)
        new_goal.user = request.user
        new_goal.save()
        return redirect(reverse('home'))
        # do something I guess
    form = GoalForm()
    return render(request = request, template_name = 'retire/new_goal.html', context = {'goal_form':form})
