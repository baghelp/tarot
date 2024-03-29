from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import WorkCashflowForm, ChangeInIncomeForm, ChangeInExpensesForm, GoalForm, RecordDatapointForm
from django.contrib import messages
from django.http import HttpResponse
from .models import WorkCashflow, ChangeInIncome, ChangeInExpenses, Goal, Datapoint
from plotly.offline import plot
from datetime import timedelta
from guest_user.decorators import allow_guest_user
import math
import plotly.graph_objs as go
import numpy as np

# render index page
def index(request):
    return render(request = request, template_name = 'tarot/index.html')

#render about page
def about(request):
    return render(request = request, template_name = 'tarot/about.html')

@allow_guest_user
def home(request):
    if not request.user.workcashflow_set.exists():
        return redirect(reverse('tarot_app:workcashflow'))

    savings_plot = makeSavingsPlot(request, default_num_dates=150)
    plot_div = [savings_plot]

    work_cashflow = request.user.workcashflow_set.all()
    changes_in_income = request.user.changeinincome_set.all()
    changes_in_expenses = request.user.changeinexpenses_set.all()
    recorded_datapoints = request.user.datapoint_set.all()
    goals = request.user.goal_set.all()

    sorted_changes_in_income = sorted(changes_in_income, key = lambda x:x.start_date)
    sorted_changes_in_expenses = sorted(changes_in_expenses, key = lambda x:x.start_date)
    sorted_datapoints = sorted(recorded_datapoints, key = lambda x:x.observed_date)
    sorted_goals = goals #sorted(goals, key = lambda x:x.goal_date)# TODO: not sorted at all

    context_to_pass = {
        "plot_div":plot_div,
        "work_cashflow":work_cashflow,
        "sorted_changes_in_income":sorted_changes_in_income,
        "sorted_changes_in_expenses":sorted_changes_in_expenses,
        "sorted_datapoints":sorted_datapoints,
        "sorted_goals":sorted_goals,
    }

    return render(request = request, template_name = 'tarot/home.html', context = context_to_pass)

@allow_guest_user
def workcashflow(request):#, id=None):

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
        return redirect(reverse('tarot_app:home'))

    elif request.POST and form.is_valid(): # only save if POST. Otherwise they want to _see_ something, not _submit_ something
        form.save()

        # save was successful, redirect
        return redirect(reverse('tarot_app:home'))
    return render(request = request, template_name = 'tarot/income_and_spending.html', context = {'workcashflow_form':form, 'can_delete':can_delete})

@allow_guest_user
def changeinincome(request, id=None):
    if id:  #user is accessing an existing change in income
        instance = get_object_or_404( ChangeInIncome, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False

        ordered_change_in_income = request.user.changeinincome_set.order_by('-start_date')
        existing_work_cashflow = request.user.workcashflow_set.all()
        if ordered_change_in_income:
            initial_income = ordered_change_in_income[0].new_yearly_income
        elif existing_work_cashflow:
            initial_income = existing_work_cashflow[0].yearly_income
        else:
            initial_income = 0
        instance = ChangeInIncome(user = request.user, new_yearly_income = initial_income)

    form = ChangeInIncomeForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        # delete was successful, redirect
        return redirect(reverse('tarot_app:home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('tarot_app:home'))

    return render(request = request, template_name = 'tarot/change_in_income.html', context = {'changeinincome_form':form, 'can_delete':can_delete})

@allow_guest_user
def changeinexpenses(request, id=None):
    if id:
        instance = get_object_or_404( ChangeInExpenses, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False
        ordered_change_in_expenses = request.user.changeinexpenses_set.order_by('-start_date')
        existing_work_cashflow = request.user.workcashflow_set.all()
        if ordered_change_in_expenses:
            initial_expenses = ordered_change_in_expenses[0].new_yearly_expenses
        elif existing_work_cashflow:
            initial_expenses = existing_work_cashflow[0].yearly_expenses
        else:
            initial_expenses = 0
        instance = ChangeInExpenses(user = request.user, new_yearly_expenses = initial_expenses)

    form = ChangeInExpensesForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        return redirect(reverse('tarot_app:home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('tarot_app:home'))

    return render(request = request, template_name = 'tarot/change_in_expenses.html', context = {'changeinexpenses_form':form, 'can_delete':can_delete})

@allow_guest_user
def recordobservation(request, id=None):
    if id:  #user is accessing an existing datapoint
        instance = get_object_or_404( Datapoint, pk=id)
        if instance.user != request.user:
            return HttpResponseForbidden()
        can_delete = True
    else:
        can_delete = False

        ordered_datapoints = request.user.datapoint_set.order_by('-observed_date')
        if ordered_datapoints:
            initial_value = ordered_datapoints[0].observed_amount
        else:
            initial_value = 0
        instance = Datapoint(user = request.user, observed_amount = initial_value)

    form = RecordDatapointForm(request.POST or None, instance = instance)
    if can_delete and request.POST.get('delete'):
        instance.delete()
        # delete was successful, redirect
        return redirect(reverse('tarot_app:home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('tarot_app:home'))

    return render(request = request, template_name = 'tarot/record_observation.html', context = {'recorddatapoint_form':form, 'can_delete':can_delete})

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
        return redirect(reverse('tarot_app:home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('tarot_app:home'))

    return render(request = request, template_name = 'tarot/one_time_investment.html', context = {'onetimeinvestment_form':form, 'can_delete':can_delete})

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
        return redirect(reverse('tarot_app:home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('tarot_app:home'))

    return render(request = request, template_name = 'tarot/recurring_investment.html', context = {'recurringinvestment_form':form, 'can_delete':can_delete})

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
        return redirect(reverse('tarot_app:home'))

    if request.POST and form.is_valid():
        form.save()
        return redirect(reverse('tarot_app:home'))

    return render(request = request, template_name = 'tarot/goal.html', context = {'goal_form':form, 'can_delete':can_delete})

def calculateDateArray(start_date, default_num_dates, goals):

    # we don't plot any data before a work_cashflow or investment of some kind starts
    num_date_buckets = default_num_dates  # initialize to reasonable value

    # if there is a goal, we make the final date the furthest-out goal date
    if goals and any([goal.goal_date for goal in goals]):
        goal_date = max([goal.goal_date for goal in goals if goal.goal_date]) + timedelta(days=30*3)  # if they have a goal, we also show 3 months after the goal
    else:
        goal_date = start_date + timedelta(days=365*10)

    date_range = goal_date - start_date
    date_delta = timedelta(days = 1) # we calculate money for every single day
    num_steps_in_date_array = math.ceil(date_range / date_delta)
    date_array = [start_date + date_delta*step for step in range(num_steps_in_date_array) if start_date + date_delta*step <= goal_date ]

    date_axis_start = start_date - 30*date_delta
    date_axis_end = goal_date + 30*date_delta

    return date_array, date_axis_start, date_axis_end

def calculate_amount_to_distribute(work_cashflow, changes_in_income, changes_in_expenses, date_array):
    # assuming that work_cashflow directly contributes to savings, calculate the savings at each day
    starting_savings = work_cashflow.starting_savings
    net_income_changes = [item for item in (changes_in_income + changes_in_expenses)]
    sorted_net_income_changes = sorted(net_income_changes, key = lambda x:x.start_date)
    net_income_change_d = {}

    # fill first element of dict
    normalized_income = work_cashflow.yearly_income * (1 / 365)
    normalized_expenses = work_cashflow.yearly_expenses * (1 / 365)

    normalized_net_income_d = {}
    normalized_net_income_d[work_cashflow.start_date] = normalized_income - normalized_expenses
    for item in sorted_net_income_changes:
        if isinstance(item, ChangeInIncome):
            normalized_income = item.new_yearly_income * 1 / 365
        elif isinstance(item, ChangeInExpenses):
            normalized_expenses = item.new_yearly_expenses * 1 / 365
        else:
            raise TypeError('The sorted_net_income_changes array should be made of exclusively income or expenses')
        normalized_net_income_d[item.start_date] = normalized_income - normalized_expenses
    normalized_net_income_d[date_array[-1]] = 0  # bookend signals the end of calculations

    amount_to_distribute = [starting_savings]
    for index, key in enumerate(normalized_net_income_d.keys()):
        this_date = key
        if index > 0:
            num_steps = math.ceil( (this_date - prev_date) / timedelta(days = 1) )
            amount_to_distribute += [amount_to_distribute[-1] + normalized_net_income*step for step in range(1,num_steps)]
        normalized_net_income = normalized_net_income_d[key]
        prev_date = this_date - timedelta(days=1)
    return np.array(amount_to_distribute)

def calculate_savings(work_cashflow, amount_to_distribute):
    savings = np.clip(amount_to_distribute, a_min=0, a_max=work_cashflow.amount_kept_in_savings)
    amount_to_distribute_remaining = amount_to_distribute - savings
    return savings, amount_to_distribute_remaining

def calculate_retirement(work_cashflow, amount_to_distribute_remaining, date_array):
    added_daily_to_retirement = work_cashflow.added_yearly_to_retirement / 365
    add_to_retirement = np.array([added_daily_to_retirement]*len(date_array))
    cumulative_added_to_retirement = np.clip(np.cumsum(add_to_retirement), a_min=0, a_max=amount_to_distribute_remaining)
    amount_to_distribute_remaining = amount_to_distribute_remaining - cumulative_added_to_retirement
    retirement_delta = np.diff(cumulative_added_to_retirement)
    retirement = [work_cashflow.starting_retirement + retirement_delta[0]]
    daily_growth_rate = (1+float(work_cashflow.retirement_yearly_growth_rate)/100)**(1/365)
    for delta in retirement_delta[0:]:
        retirement.append(retirement[-1]*daily_growth_rate + delta)
    return np.array(retirement), amount_to_distribute_remaining


def calculate_money_market(work_cashflow, amount_to_distribute_remaining, date_array):
    money_market_investment = np.diff(amount_to_distribute_remaining)
    daily_growth_rate = (1+float(work_cashflow.other_investment_yearly_growth_rate)/100)**(1/365)
    money_market = [amount_to_distribute_remaining[0]]
    for delta in money_market_investment:
        money_market.append(money_market[-1]*daily_growth_rate + delta)
    return np.array(money_market)

def get_observations(observations, observation_type):
    observation_values_array = []
    observation_dates_array = []
    for ob in observations:  # possibly bug here
        if ob.monetary_category == observation_type:
            observation_values_array.append(ob.observed_amount)
            observation_dates_array.append(ob.observed_date)
    return np.array(observation_values_array), np.array(observation_dates_array)

def calculate_goal_array(goals, date_array):
    goals_array = []
    for goal in goals:
        daily_growth_rate = (1+float(goal.assumed_yearly_inflation)/100)**(1/365)
        start_date = date_array[0]
        days_from_start_to_value_date = int( (start_date - goal.dollar_value_date) / timedelta(days=1))
        value_at_start_date = goal.goal_amount*daily_growth_rate**days_from_start_to_value_date

        num_steps = int((date_array[-1] - start_date) / timedelta(days = 1))
        goal_array = [value_at_start_date*daily_growth_rate**step for step in range(num_steps)]
        goals_array.append(goal_array)
    return goals_array


def makeSavingsPlot(request, default_num_dates):
    work_cashflow = request.user.workcashflow_set.first()
    changes_in_income = list(request.user.changeinincome_set.all())
    changes_in_expenses = list(request.user.changeinexpenses_set.all())
    recorded_datapoints = request.user.datapoint_set.all()
    goals = list(request.user.goal_set.all())

    # sort the arrays #TODO: we can probably store these arrays sorted instead of resorting every time
    sorted_changes_in_income = sorted(changes_in_income, key = lambda x:x.start_date)
    sorted_changes_in_expenses = sorted(changes_in_expenses, key = lambda x:x.start_date)
    sorted_datapoints = sorted(recorded_datapoints, key = lambda x:x.observed_date)

    date_array, date_axis_start, date_axis_end = calculateDateArray( work_cashflow.start_date, default_num_dates, goals)

    amount_to_distribute = calculate_amount_to_distribute(work_cashflow, changes_in_income, changes_in_expenses, date_array)
    savings_array, amount_to_distribute_remaining = calculate_savings(work_cashflow, amount_to_distribute)
    retirement_array, amount_to_distribute_remaining =  calculate_retirement(work_cashflow, amount_to_distribute_remaining, date_array)
    money_market_array = calculate_money_market(work_cashflow, amount_to_distribute_remaining, date_array)
    goals_values = calculate_goal_array(goals, date_array)

    net_worth_array = savings_array + retirement_array + money_market_array

    net_worth_observations_array, net_worth_observation_dates = get_observations(sorted_datapoints, 'net worth')
    retirement_observations_array, retirement_observation_dates = get_observations(sorted_datapoints, 'retirement value')
    money_market_observations_array, money_market_observation_dates = get_observations(sorted_datapoints, 'invested value')

    net_worth = go.Scatter(x = date_array, 
                      y = net_worth_array,
                      mode = 'lines', 
                      name = 'projected net worth',
                      opacity = 0.8, 
                      marker_color = '#2ca02c')

    net_worth_observations = go.Scatter(x = net_worth_observation_dates, 
                      y = net_worth_observations_array,
                      mode = 'markers', 
                      name = 'actual net worth',
                      opacity = 0.8, 
                      marker_color = '#2ca02c')

    savings = go.Scatter(x = date_array, 
                      y = savings_array,
                      mode = 'lines', 
                      name = 'projected savings',
                      opacity = 0.8,
                      marker_color = '#d62728')

    retirement = go.Scatter(x = date_array, 
                      y = retirement_array,
                      mode = 'lines', 
                      name = 'projected retirement',
                      opacity = 0.8,
                      marker_color = '#17becf')

    retirement_observations = go.Scatter(x = retirement_observation_dates, 
                      y = retirement_observations_array,
                      mode = 'markers', 
                      name = 'actual retirement value',
                      opacity = 0.8, 
                      marker_color = '#17becf')

    money_market = go.Scatter(x = date_array, 
                      y = money_market_array,
                      mode = 'lines', 
                      name = 'projected investments',
                      opacity = 0.8,
                      marker_color = '#9467bd')

    money_market_observations = go.Scatter(x = money_market_observation_dates, 
                      y = money_market_observations_array,
                      mode = 'markers', 
                      name = 'actual investments value',
                      opacity = 0.8,
                      marker_color = '#9467bd')

    layout = go.Layout( paper_bgcolor='#fbfbfb',
                        plot_bgcolor='#DDDDDD',
                        margin = go.layout.Margin( t=0),
                        legend = dict(x = 0, y = 1, bgcolor = 'rgba(0,0,0,0)'),
                        )

    layout.yaxis.gridcolor = 'black'
    layout.xaxis.gridcolor = 'black'
    layout.xaxis.range = [date_axis_start, date_axis_end]
    layout.title.x = 0.5
    data = [net_worth, savings, retirement, money_market]

    for i, item in enumerate(goals_values):
        data.append( go.Scatter(x = date_array,
                                y = item,
                                mode = 'lines',
                                name = goals[i].name,
                                opacity = 0.8)
        )
        
    data += [net_worth_observations, retirement_observations, money_market_observations]


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
        return redirect(reverse('tarot_app:home'))
        # do something I guess
    form = GoalForm()
    return render(request = request, template_name = 'tarot/new_goal.html', context = {'goal_form':form})
