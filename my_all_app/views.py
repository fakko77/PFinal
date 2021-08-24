from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import IndexForm, IndicatorForm, PositionForm, CalculatorForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Index, Indicator, Position
from django.db.models import Q
import requests
import json

#avec selection

def view_login(request):
    """view that allows view for login"""
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
    """home"""
    if request.user.is_authenticated:
        win = Position.objects.filter(user=request.user.id, status="win")
        defeat = Position.objects.filter(user=request.user.id, status="defeat")
        context = {
            'win': win,
            'defeat': defeat,
        }
        return render(request, 'my_all_app/index.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def add(request):
    """view that allows add a new position """
    if request.user.is_authenticated:
        form = PositionForm(request.POST or None, request.FILES or None)
        context = {
            'form': form,
        }
        if request.method == 'POST':
            if form.is_valid():
                print("etape 3")
                user = request.user.id
                position_index = form.cleaned_data.get('position_index')
                volume = form.cleaned_data.get('volume')
                price = "0004"
                be = form.cleaned_data.get('be')
                tp1 = form.cleaned_data.get('tp1')
                tp2 = form.cleaned_data.get('tp2')
                position_indicator = form.cleaned_data.get(
                    'position_indicator')
                comment = form.cleaned_data.get(
                    'comment')
                print(position_index, position_indicator)
                PositionNew = Position(position_index=position_index,
                                       volume=volume, price=price, be=be, tp1=tp1,
                                       tp2=tp2, comment=comment, user=user)
                PositionNew.save()
                for position_indicator in position_indicator:
                    object = Indicator.objects.get(name=position_indicator.name)
                    PositionNew.position_indicator.add(object.id)
                PositionNew.save()

            else:
                print(form.errors)
        return render(request, 'my_all_app/add.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def manage(request):
    """view that allows Manage position"""
    if request.user.is_authenticated:
        historic = Position.objects.filter(user=request.user.id, status=None)
        historic = historic.order_by('date').reverse()
        paginator = Paginator(historic, 6)
        page = request.GET.get('page')
        try:
            historic = paginator.page(page)
        except PageNotAnInteger:
            historic = paginator.page(1)
        except EmptyPage:
            historic = paginator.page(paginator.num_pages)
        context = {
            'hist': historic,
        }
        return render(request, 'my_all_app/manage.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def history(request):
    """ view that allows show all history of position """
    if request.user.is_authenticated:
        historic = Position.objects.filter(user=request.user.id)
        historic = historic.exclude(status=None)
        historic = historic.order_by('date').reverse()
        paginator = Paginator(historic, 6)
        page = request.GET.get('page')
        try:
            historic = paginator.page(page)
        except PageNotAnInteger:
            historic = paginator.page(1)
        except EmptyPage:
            historic = paginator.page(paginator.num_pages)
        context = {
            'hist': historic,
        }
        return render(request, 'my_all_app/history.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def calculator(request):
    """view which allows to calculate """
    form = CalculatorForm(request.POST or None, request.FILES or None)
    context = {
        'formcal': form,
    }
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                try:
                    index1 = request.POST.get('Index')
                    index2 = "EUR" + index1[0:3]
                    print(index2)
                    balance = form.cleaned_data.get('balance')
                    risk = form.cleaned_data.get('risk')
                    sl = form.cleaned_data.get('sl')
                    r1 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                      + index1 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    price = r1.json()[0]['price']
                    r2 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                      + index2 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    convert = r2.json()[0]['price']
                    print(price)
                    result = round(
                        (float(balance) * float(convert)) * (float(risk) / 100) * float(price) / (float(sl) * 10), 2)
                    print(result)
                    context = {
                        'formcal': form,
                        'money': result,
                    }

                except IndexError:

                    index1 = request.POST.get('Index')
                    index2 = index1[0:3] + "EUR"
                    print(index2)
                    balance = form.cleaned_data.get('balance')
                    risk = form.cleaned_data.get('risk')
                    sl = form.cleaned_data.get('sl')
                    r1 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                      + index1 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    price = r1.json()[0]['price']
                    convert = 1
                    print(price)
                    result = round(
                        (float(balance) * float(convert)) * (float(risk) / 100) * float(price) / (float(sl) * 10), 2)
                    print(result)
                    context = {
                        'formcal': form,
                        'money': result,
                    }
        return render(request, 'my_all_app/calculator.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def setting(request):
    """ view that allows configure this app"""
    if request.user.is_authenticated:

        idexAll = Index.objects.filter(user=request.user.id)
        IndicatorAll = Indicator.objects.filter(user=request.user.id)
        form1 = IndexForm(request.POST)
        tab = []
        print(len(idexAll))
        i = 0
        while i < len(idexAll):
            tab.append(idexAll[i].name)
            i += 1
        r1 = requests.get('https://financialmodelingprep.com/api/v3/symbol/'
                          'available-forex-currency-pairs?apikey=be0024b5e186d1842ee2a98a37e4169b')
        i = 0
        tabList = []
        for symbol in r1.json():
            tabList.append(r1.json()[i]['symbol'])
            i += 1
        print(len(tabList))
        print(tabList)
        for tab in tab:
            i = 0
            while i < len(tabList):
                if tabList[i] == tab:
                    tabList.remove(tab)
                i += 1
        print(tabList)
        """
        for idexAll in idexAll:
            tab.append(idexAll.name)
        
        """
        form2 = IndicatorForm(request.POST)
        context = {
            'form': form1,
            'form2': form2,
            'all': idexAll,
            'indexDispo': tabList,
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
                user = request.user.id
                name = form1.cleaned_data.get('name')
                index_add = Index(name=name, user=user)
                index_add.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                pass
        return render(request, 'my_all_app/setting.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def indexDelete(request, indexid):
    """ view that allows delete a index  """
    index = Index.objects.get(id=indexid)
    index.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def IndicatorDelete(request, indicatorid):
    """ view that allows delete a indicator  """
    indicator = Indicator.objects.get(id=indicatorid)
    indicator.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def positionDelete(request, positionid):
    """ view that allows delete a postion  """
    position = Position.objects.get(id=positionid)
    position.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def positionWin(request, positionid):
    """ view that allows close in profit """
    position = Position.objects.get(id=positionid)
    position.status = "win"
    position.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def positionDefeat(request, positionid):
    """view that close in defeat """
    position = Position.objects.get(id=positionid)
    position.status = "defeat"
    position.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
