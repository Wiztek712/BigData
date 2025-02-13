from django.shortcuts import render

def loghome(request):
    return render(request, 'loghome.html')

def home(request):
    return render(request, 'home.html')