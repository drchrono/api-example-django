from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import Context
from django.template.context_processors import csrf
from django.views.generic import View

import requests
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from .forms import PatientForm
from .models import Patient, Doctor


@login_required(login_url='/login/')
def home(request):
  context = Context({'username' : request.user.username })
  return render(request, 'index.html', context)

@login_required(login_url='/login/')
def logout(request):
  auth_logout(request)
  return redirect(home)

@login_required(login_url='/login/')
def patient_signin(request):
  if request.method == 'POST':
    form = PatientForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      return redirect(thanks)
  else:
    form = PatientForm()
  
  context = Context({ 'form': form })
  context.update(csrf(request))
  return render(request, 'patient.html', context)

@login_required(login_url='/login/')
def thanks(request):
  return render(request, 'thanks.html')