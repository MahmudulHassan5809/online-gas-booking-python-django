from django import forms
from django.forms import FileInput
from gas.models import Connection, Booking, Staff, Stock
from django.contrib.auth import get_user_model

User = get_user_model()


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('user', 'mobile', 'address')

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=True)


class ConnectionForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('1', 'Male'),
        ('2', 'Female')
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Connection
        exclude = ('user', 'status',)

    def clean(self):
        if not self.update:
            check_user_connection = Connection.objects.filter(
                user=self.user).first()
            if check_user_connection:
                raise forms.ValidationError(
                    "You Already Have A Connection.Please Update...")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.update = kwargs.pop('update', None)
        super(ConnectionForm, self).__init__(*args, **kwargs)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('reffiling',)

    def clean_reffiling(self):
        reffiling = self.cleaned_data.get('reffiling')
        stock_obj = Stock.objects.get(gas_reffiling_id=reffiling)
        if stock_obj.quantity <= 0:
            raise forms.ValidationError(
                "Sorry This Cylinder Is Not Avialable Now.")
        return reffiling

    def clean(self):
        check_user_connection = Connection.objects.filter(
            user=self.user).first()
        if check_user_connection.status != '1':
            raise forms.ValidationError(
                "Please Wait Your Connection Still Not Approved.")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookingForm, self).__init__(*args, **kwargs)
