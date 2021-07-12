from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import IndexForm, IndicatorForm, PositionForm, CalculatorForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Index, Indicator, Position
from django.http import HttpResponseRedirect
from django.db.models import Q
import requests
import json


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
        form = PositionForm(request.POST)
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
                position_indicator = form.cleaned_data.get('position_indicator')
                comment = form.cleaned_data.get('comment')
                PositionNew = Position(position_index=position_index, volume=volume, price=price, be=be, tp1=tp1,
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
    if request.user.is_authenticated:
        Historique = Position.objects.filter(user=request.user.id, status=None)
        Historique = Historique.order_by('date').reverse()
        paginator = Paginator(Historique, 6)
        page = request.GET.get('page')
        try:
            Historique = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            Historique = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            Historique = paginator.page(paginator.num_pages)

        context = {
            'hist': Historique,
        }
        return render(request, 'my_all_app/manage.html',context)
    else:
        return render(request, 'my_all_app/login.html')


def history(request):
    if request.user.is_authenticated:
        Historique = Position.objects.filter(user=request.user.id)
        Historique = Historique.exclude(status=None)
        Historique = Historique.order_by('date').reverse()


        paginator = Paginator(Historique, 6)
        page = request.GET.get('page')
        try:
            Historique = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            Historique = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            Historique = paginator.page(paginator.num_pages)

        context = {
            'hist': Historique,
        }
        return render(request, 'my_all_app/history.html', context)
    else:
        return render(request, 'my_all_app/login.html')


def calculator(request):
    formcal = CalculatorForm(request.POST)
    idexAll = Index.objects.filter(user=request.user.id)
    context = {
        'index': idexAll,
        'formcal': formcal,
    }
    if request.user.is_authenticated:
        if request.method == 'POST':
            if formcal.is_valid():
                try:
                    index1 = request.POST.get('Index')
                    index2 = "EUR" + index1[0:3]
                    print(index2)
                    balance = formcal.cleaned_data.get('balance')
                    risk = formcal.cleaned_data.get('risk')
                    sl = formcal.cleaned_data.get('sl')
                    r1 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                        + index1 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    price = r1.json()[0]['price']
                    r2 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                        + index2 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    convert = r2.json()[0]['price']
                    print(price)
                    result = round((float(balance) * float(convert)) * (float(risk)/100) * float(price) / (float(sl) * 10),2)
                    print(result)
                    context = {
                        'index': idexAll,
                        'money': result,
                    }

                except IndexError:

                    index1 = request.POST.get('Index')
                    index2 = index1[0:3] + "EUR"
                    print(index2)
                    balance = formcal.cleaned_data.get('balance')
                    risk = formcal.cleaned_data.get('risk')
                    sl = formcal.cleaned_data.get('sl')
                    r1 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                      + index1 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    price = r1.json()[0]['price']
                    convert = 1
                    print(price)
                    result = round((float(balance) * float(convert)) * (float(risk) / 100) * float(price) / (float(sl) * 10),2)
                    print(result)
                    context = {
                        'index': idexAll,
                        'money': result,
                    }


            """
            index = request.POST.get('indexselect')
            volume = request.POST.get('volume', False)
            sl = request.POST.get('sl', False)
            print("hooooooooooooo", index, volume , sl)
            r = requests.get('https://financialmodelingprep.com/api/v3/quote/'+ index + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
            price = r.json()[0]['price']
            eur = float((0.0001 * (float(volume) * 100000)/float(price)) * float(sl))
            resultat = round(eur,2)
            context = {
                'index': idexAll,
                'money': resultat,
            }
            """
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


def positionDelete(request, positionId):
    position = Position.objects.get(id=positionId)
    position.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def positionWin(request, positionId):
    postion = Position.objects.get(id=positionId)
    postion.status = "win"
    postion.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def positionDefeat(request, positionId):
    postion = Position.objects.get(id=positionId)
    postion.status = "defeat"
    postion.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))






