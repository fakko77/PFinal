from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from .forms import IndexForm, IndicatorForm, PositionForm, CalculatorForm, UserCreationForm, EmailChangeForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Index, Indicator, Position
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import requests



def view_login(request):
    """view that allows view for login"""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'my_all_app/index.html')
    return render(request, 'registration/login.html')


def index(request):
    """view index show all info of the account """
    if request.user.is_authenticated:
        win = Position.objects.filter(user=request.user.id, status="win")
        defeat = Position.objects.filter(user=request.user.id, status="defeat")
        context = {
            'win': win,
            'defeat': defeat,
        }
        return render(request, 'my_all_app/index.html', context)
    else:
        return render(request, 'registration/login.html')


def add(request):
    """view that allows add a new position """
    if request.user.is_authenticated:
        form = PositionForm(request.POST or None, request.FILES or None)
        index = Index.objects.filter(user=request.user.id)
        IndicatorAll = Indicator.objects.filter(user=request.user.id)
        context = {
            'form': form,
            'index': index,
            'indicator': IndicatorAll,
        }
        if request.method == 'POST':
            if form.is_valid():
                user = request.user.id
                position_index = request.POST.get('position_index')
                volume = form.cleaned_data.get('volume')
                r1 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                  + str(position_index) + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                price = r1.json()[0]['price']
                sl = form.cleaned_data.get('sl')
                be = form.cleaned_data.get('be')
                tp1 = form.cleaned_data.get('tp1')
                tp2 = form.cleaned_data.get('tp2')
                position_indicator = request.POST.getlist('position_indicator')
                comment = form.cleaned_data.get(
                    'comment')
                INDEX = Index.objects.get(name=position_index)
                PositionNew = Position(position_index=INDEX,
                                       volume=volume, price=price, sl=sl, be=be, tp1=tp1,
                                       tp2=tp2, comment=comment, user=user)
                PositionNew.save()
                for position_indicator in position_indicator:
                    object = Indicator.objects.get(id=position_indicator)
                    PositionNew.position_indicator.add(object.id)
                PositionNew.save()
                return redirect('manage')
            else:
                print(form.errors)
        return render(request, 'my_all_app/add.html', context)
    else:
        return render(request, 'registration/login.html')


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
        return render(request, 'registration/login.html')


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
        return render(request, 'registration/login.html')


def calculator(request):
    """view which allows to calculate """
    form = CalculatorForm(request.POST or None, request.FILES or None)
    index = Index.objects.filter(user=request.user.id)
    context = {
        'formcal': form,
        'index': index,
    }
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                try:
                    index1 = request.POST.get('position_index')
                    print(index1)
                    index2 = "EUR" + index1[0:3]
                    balance = form.cleaned_data.get('balance')
                    risk = form.cleaned_data.get('risk')
                    sl = form.cleaned_data.get('sl')
                    r1 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                      + index1 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    price = r1.json()[0]['price']
                    r2 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                      + index2 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    convert = r2.json()[0]['price']
                    result = round(
                        (float(balance) * float(convert)) *
                        (float(risk) / 100) * float(price) / (float(sl) * 10), 2)
                    context = {
                        'formcal': form,
                        'money': result,
                    }

                except IndexError:

                    index1 = request.POST.get('position_index')
                    index2 = index1[0:3] + "EUR"
                    balance = form.cleaned_data.get('balance')
                    risk = form.cleaned_data.get('risk')
                    sl = form.cleaned_data.get('sl')
                    r1 = requests.get('https://financialmodelingprep.com/api/v3/quote/'
                                      + index1 + '?apikey=be0024b5e186d1842ee2a98a37e4169b')
                    price = r1.json()[0]['price']
                    convert = 1
                    result = round(
                        (float(balance) * float(convert)) *
                        (float(risk) / 100) * float(price) / (float(sl) * 10), 2)
                    context = {
                        'formcal': form,
                        'money': result,
                        'index': index,
                    }
        return render(request, 'my_all_app/calculator.html', context)
    else:
        return render(request, 'registration/login.html')


def setting(request):
    """ view that allows configure this app"""
    if request.user.is_authenticated:

        indexAll = Index.objects.filter(user=request.user.id)

        IndicatorAll = Indicator.objects.filter(user=request.user.id)

        form1 = IndexForm(request.POST)
        tab = []
        i = 0

        while i < len(indexAll):
            tab.append(indexAll[i].name)
            i += 1
        r1 = requests.get('https://financialmodelingprep.com/api/v3/symbol/'
                          'available-forex-currency-pairs?apikey=be0024b5e186d1842ee2a98a37e4169b')
        i = 0
        tabList = []
        for symbol in r1.json():
            tabList.append(r1.json()[i]['symbol'])
            i += 1
        for tab in tab:
            i = 0
            while i < len(tabList):
                if tabList[i] == tab:
                    tabList.remove(tab)
                i += 1

        form2 = IndicatorForm(request.POST)
        context = {
            'form': form1,
            'form2': form2,
            'all': indexAll,
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
        return render(request, 'registration/login.html')


def index_delete(request, indexId):
    """ view that allows delete a index  """
    index = Index.objects.get(id=indexId)
    index.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def indicator_delete(request, indicatorId):
    """ view that allows delete a indicator  """
    indicator = Indicator.objects.get(id=indicatorId)
    indicator.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def position_delete(request, positionId):
    """ view that allows delete a postion  """
    position = Position.objects.get(id=positionId)
    position.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def position_win(request, positionId):
    """ view that allows close in profit """
    position = Position.objects.get(id=positionId)
    position.status = "win"
    position.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def position_defeat(request, positionId):
    """view that close in defeat """
    position = Position.objects.get(id=positionId)
    position.status = "defeat"
    position.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_password(request):
    """view for edit password of account"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('change_password')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)

        return render(request, 'my_all_app/editAccount.html', {'form': form})
    else:
        return render(request, 'registration/login.html')


def signup(request):
    """View for sign up on app"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'my_all_app/index.html')
    else:
        form = UserCreationForm()
        print(form.errors, len(form.errors))
    return render(request, 'my_all_app/signup.html', {'form': form})


def edit_position(request, positionId):
    """view for edit password of account"""
    if request.user.is_authenticated:
        index = Index.objects.filter(user=request.user.id)
        IndicatorAll = Indicator.objects.filter(user=request.user.id)
        position = Position.objects.get(id=positionId)
        form = PositionForm(request.POST or None, instance=position)
        context = {
            'form': form,
            'index': index,
            'indicator': IndicatorAll,
        }
        if form.is_valid():
            form.save()
            return redirect('manage')
        else:
            print('error')
            print(form.errors, len(form.errors))
        return render(request, 'my_all_app/editPosition.html', context)
    else:
        return render(request, 'registration/login.html')


def edit_email(request):
    """view for edit password of account"""
    if request.user.is_authenticated:
        form = EmailChangeForm(request.user, request.POST)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            return render(request, "my_all_app/editEmail.html", {'form': form})

