from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import IndexForm , IndicatorForm
from .models import Index , Indicator
from django.http import HttpResponseRedirect


def view_login(request):
    """view for login"""
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'my_all_app/index.html')
        return render(request, 'my_all_app/login.html')
    return render(request, 'my_all_app/login.html')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'my_all_app/index.html')
    else:
        return render(request, 'my_all_app/login.html')


def add(request):
    if request.user.is_authenticated:
        return render(request, 'my_all_app/add.html')
    else:
        return render(request, 'my_all_app/login.html')


def manage(request):
    if request.user.is_authenticated:
        return render(request, 'my_all_app/manage.html')
    else:
        return render(request, 'my_all_app/login.html')


def history(request):
    if request.user.is_authenticated:
        return render(request, 'my_all_app/history.html')
    else:
        return render(request, 'my_all_app/login.html')


def calculator(request):
    idexAll = Index.objects.filter(user=request.user.id)
    context = {
        'index': idexAll,
    }
    if request.user.is_authenticated:
        return render(request, 'my_all_app/calculator.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def setting(request):
    if request.user.is_authenticated:
        idexAll = Index.objects.filter(user=request.user.id)
        IndicatorAll = Indicator.objects.filter(user=request.user.id)
        form1 = IndexForm(request.POST)
        form2 = IndicatorForm(request.POST)
        context = {
            'form': form1,
            'form2': form2,
            'all':idexAll,
            'indicator': IndicatorAll,
        }
        if request.method == "POST":
            if form2.is_valid():
                user = request.user.id
                name = form2.cleaned_data.get('name')
                description = form2.cleaned_data.get('description')
                indicator_add = Indicator(name=name, description=description, user=user)
                indicator_add.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif form1.is_valid():
                user  = request.user.id
                name  = form1.cleaned_data.get('name')
                index_add = Index(name=name,user=user)
                index_add.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                pass
        return render(request, 'my_all_app/setting.html',context)
    else:
        return render(request, 'my_all_app/login.html')

def indexDelete(request, indexId):
    index = Index.objects.get(id=indexId)
    index.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def IndicatorDelete(request, indicatorId):
    indicator = Indicator.objects.get(id=indicatorId)
    indicator.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



