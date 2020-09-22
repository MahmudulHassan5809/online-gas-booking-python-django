from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .models import Profile, PaymentCreditCard
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import date, datetime
from calendar import monthrange


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            label=_("E-mail"), max_length=75)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class SignUpForm(UserCreationForm):

    phone_number = forms.CharField(
        label='Phone Number', widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phone_number',
                  'password1', 'password2', )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'User Name'}),
            # 'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            # 'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'type': 'email'}),

        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': "Password"})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': "Confirm Password"})

        self.fields['email'].required = True
        # self.fields['first_name'].required = True
        # self.fields['last_name'].required = True
        self.fields['phone_number'].required = True


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address',)


class CreditCardField(forms.IntegerField):
    @staticmethod
    def get_cc_type(number):
        number = str(number)
        # group checking by ascending length of number
        if len(number) == 13:
            if number[0] == "4":
                return "Visa"
        elif len(number) == 14:
            if number[:2] == "36":
                return "MasterCard"
        elif len(number) == 15:
            if number[:2] in ("34", "37"):
                return "American Express"
        elif len(number) == 16:
            if number[:4] == "6011":
                return "Discover"
            if number[:2] in ("51", "52", "53", "54", "55"):
                return "MasterCard"
            if number[0] == "4":
                return "Visa"
        return "Unknown"

    def clean(self, value):
        """Check if given CC number is valid and one of the
           card types we accept"""
        if value and (len(value) < 13 or len(value) > 16):
            raise forms.ValidationError("Please enter in a valid " +
                                        "credit card number.")
        elif self.get_cc_type(value) not in ("Visa", "MasterCard",
                                             "American Express"):
            raise forms.ValidationError("Please enter in a Visa, " +
                                        "Master Card, or American Express credit card number.")
        return super(CreditCardField, self).clean(value)


class CCExpWidget(forms.MultiWidget):
    """ Widget containing two select boxes for selecting the month and year"""

    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]

    def format_output(self, rendered_widgets):
        html = u' / '.join(rendered_widgets)
        return u'<span style="white-space: nowrap">%s</span>' % html


class CCExpField(forms.MultiValueField):
    EXP_MONTH = [(x, x) for x in range(1, 13)]
    EXP_YEAR = [(x, x) for x in range(date.today().year,
                                      date.today().year + 15)]
    default_error_messages = {
        'invalid_month': u'Enter a valid month.',
        'invalid_year': u'Enter a valid year.',
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.ChoiceField(choices=self.EXP_MONTH,
                              error_messages={'invalid': errors['invalid_month']}),
            forms.ChoiceField(choices=self.EXP_YEAR,
                              error_messages={'invalid': errors['invalid_year']}),
        )
        super(CCExpField, self).__init__(fields, *args, **kwargs)
        self.widget = CCExpWidget(widgets=[fields[0].widget, fields[1].widget])

    def clean(self, value):
        exp = super(CCExpField, self).clean(value)
        if date.today() > exp:
            raise forms.ValidationError(
                "The expiration date you entered is in the past.")
        return exp

    def compress(self, data_list):
        if data_list:

            if not data_list[1]:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if not data_list[0]:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)
            year = int(data_list[1])
            month = int(data_list[0])
            # find last day of the month
            day = monthrange(year, month)[1]
            return date(year, month, day)
        return None


class PaymentCreditCardForm(ModelForm):
    card_number = CreditCardField(required=True, label="Card Number")
    card_holder = forms.CharField(required=True, label="Card Holder Name",
                                  max_length=60)
    expiration = CCExpField(required=True, label="Expiration")
    security_code = forms.IntegerField(required=True, label="CCV Number",
                                       max_value=9999, widget=forms.TextInput(attrs={'size': '4'}))

    class Meta:
        model = PaymentCreditCard
        exclude = ('owner',)
