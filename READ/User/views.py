from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

def User(request):
    return render(request, 'User/register.html')
