from django import forms
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
        fields = ('position_index', 'volume','be','tp1','tp2','position_indicator','comment'  )

        #https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/