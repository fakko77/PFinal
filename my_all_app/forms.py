from django import forms
from my_all_app.models import Index


class IndexForm(forms.ModelForm):
    class Meta:
        model = Index
        fields = ('name',)

        #https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/