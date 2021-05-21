from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'my_all_app/index.html')

