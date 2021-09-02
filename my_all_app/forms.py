from django import forms
from django.forms import ModelForm
from my_all_app.models import Index, Indicator, Position
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import TextInput, EmailInput, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
        fields = ('volume', 'be', 'sl', 'tp1', 'tp2',
                  'position_indicator', 'comment')
        widgets = {
           # 'position_index': forms.Select(attrs={'class': 'form-control rs'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control',
                                               'step': '0.01',
                                               'min': '0.01', 'max': '5'}),
            'sl': forms.NumberInput(attrs={'class': 'form-control',
                                           'step': '1',
                                           'min': '1', 'max': '500'}),
            'be': forms.NumberInput(attrs={'class': 'form-control',
                                           'step': '1',
                                           'min': '1', 'max': '500'}),
            'tp1': forms.NumberInput(attrs={'class': 'form-control',
                                            'step': '1',
                                            'min': '1', 'max': '500'}),
            'tp2': forms.NumberInput(attrs={'class': 'form-control',
                                            'step': '1',
                                            'min': '1', 'max': '500'}),
            'position_indicator': forms.CheckboxSelectMultiple(
                attrs={'class': 'form'}),
            'comment': forms.Textarea(attrs={'class': 'form',
                                             'rows': '5', 'cols': '33'}),

        }


class CalculatorForm(forms.Form):
    pass

    """
    allPosition = Index.objects.all()
    CHOICES = []
    for allPosition in allPosition:
        a = (str(allPosition.name), str(allPosition.name))
        CHOICES.append(a)
    balance = forms.IntegerField(label='solde')
    risk = forms.IntegerField(label='RISK %')
    sl = forms.IntegerField(label='SL')
    Index = forms.ChoiceField(choices=CHOICES)
    """


class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the
    e-mail.
    """
    error_messages = {
        'email_mismatch': "The two email addresses fields didn't match.",
        'not_changed': "The email address is the same as the one already defined.",
    }

    new_email1 = forms.EmailField(
        label=("New email address"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=("New email address confirmation"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user