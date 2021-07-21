from django import forms
from django.forms import ModelForm
from my_all_app.models import Index, Indicator, Position


class IndexForm(forms.ModelForm):
    class Meta:
        model = Index
        fields = ('name',)


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ('name', 'description')


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('position_index', 'volume', 'be', 'sl', 'tp1', 'tp2', 'position_indicator', 'comment')
        widgets = {
            'position_index': forms.Select(attrs={'class': 'form-control rs'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01', 'max': '5'}),
            'sl': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '1', 'max': '500'}),
            'be': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '1', 'max': '500'}),
            'tp1': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '1', 'max': '500'}),
            'tp2': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '1', 'max': '500'}),
            'position_indicator': forms.CheckboxSelectMultiple(attrs={'class': 'form'}),
            'comment': forms.Textarea(attrs={'class': 'form',  'rows': '5', 'cols': '33'}),

        }


class CalculatorForm(forms.Form):
    allPosition = Index.objects.all()
    CHOICES = []
    for allPosition in allPosition:
        a = (str(allPosition.name), str(allPosition.name))
        CHOICES.append(a)
    balance = forms.IntegerField(label='solde')
    risk = forms.IntegerField(label='RISK %')
    sl = forms.IntegerField(label='SL')
    Index = forms.ChoiceField(choices=CHOICES)


