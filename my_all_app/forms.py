from django import forms
from my_all_app.models import Index, Indicator


class IndexForm(forms.ModelForm):
    class Meta:
        model = Index
        fields = ('name',)

class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ('name','description')

        #https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/