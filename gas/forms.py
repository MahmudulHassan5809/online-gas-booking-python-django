from django import forms
from django.forms import FileInput
from gas.models import Connection


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
