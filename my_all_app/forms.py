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
        fields = ('name','description')

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('position_index', 'volume','be','tp1','tp2', 'position_indicator','comment'  )
        widgets = {
            'position_index': forms.Select(attrs={'class': 'test'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'step':'0.01', 'min':'0.01', 'max':'5'}),
            'be': forms.NumberInput(attrs={'class': 'form-control', 'step':'1', 'min':'1', 'max':'50'}),
            'tp1': forms.NumberInput(attrs={'class': 'form-control' ,'step':'1', 'min':'1', 'max':'500'}),
            'tp2': forms.NumberInput(attrs={'class': 'form-control' ,'step':'1', 'min':'1', 'max':'500'}),
            'position_indicator': forms.CheckboxSelectMultiple(attrs={'class': 'form'}),
            'comment': forms.Textarea(attrs={'class': 'form'}),

        }


        #https://docs. djangoproject.com/en/3.2/topics/forms/modelforms/