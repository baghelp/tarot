from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from plotly.offline import plot
from datetime import timedelta
from guest_user.decorators import allow_guest_user
import math
import plotly.graph_objs as go
import numpy as np

def index(request):
    return render(request = request, template_name = 'code_immersion/index.html')

def convert(request):
    return render(request = request, template_name = 'code_immersion/convert.html')

def login(request):
    return render(request = request, template_name = 'code_immersion/login.html')

@allow_guest_user
def about(request):
    return render(request = request, template_name = 'code_immersion/about.html')

@allow_guest_user
def home(request):

    context_to_pass = {
        "plot_div":'hi',
    }

    return render(request = request, template_name = 'code_immersion/home.html', context = {})


