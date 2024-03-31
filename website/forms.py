from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Reagent, ReagentType, ContainerType, Container
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import SelectDateWidget
from .models import Reagent, Container, ReagentType


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


from django import forms
from .models import Reagent, Container, ReagentType
from django.contrib.auth.models import User


class AddReagentForm(forms.ModelForm):
    reagent_number = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"placeholder": "Reagent Number", "class": "form-control"}), label="")
    reagent_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"placeholder": "Reagent Name", "class": "form-control"}), label="")
    container_number = forms.ModelChoiceField(queryset=Container.objects.all(), required=True,
                                              widget=forms.Select(attrs={"class": "form-control"}),
                                              label="Container")
    quantity = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={"placeholder": "Quantity", "class": "form-control"}),
                               label="")
    reagent_type = forms.ModelChoiceField(queryset=ReagentType.objects.all(), required=True,
                                          widget=forms.Select(attrs={"class": "form-control"}), label="Reagent Type")
    expiration_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        attrs={"placeholder": "Expiration Date", "class": "form-control", "type": "datetime-local"}), label="")
    storage_temperature = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"placeholder": "Storage Temperature", "class": "form-control"}), label="")
    description = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={"placeholder": "Description", "class": "form-control"}),
                                  label="")
    special_instructions = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"placeholder": "Special Instructions", "class": "form-control"}), label="")
    last_usage = forms.DateTimeField(required=True, widget=forms.DateTimeInput(
        attrs={"placeholder": "Last Usage (date & time)", "class": "form-control", "type": "datetime-local"}), label="")
    last_user = forms.ModelChoiceField(queryset=User.objects.exclude(username__startswith='admin'),
                                       required=True,
                                       widget=forms.Select(attrs={"class": "form-control"}), label="Last User")

    class Meta:
        model = Reagent
        exclude = ("user",)
