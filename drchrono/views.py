from django.shortcuts import redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import Context

import requests


@login_required(login_url='/login/')
def home(request):
  context = Context({"username" : request.user.username })
  return render(request, 'index.html', context)

def logout(request):
  auth_logout(request)
  return redirect(home)
