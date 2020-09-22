from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import json


class AictiveUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_profile.active and request.user.user_profile.email_confirmed:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('Please Login Or May Be Your Account Is Not Active Or Not A Valid User'))
            return redirect('accounts:login')


class UserHasPaymentSystem:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_payment_credit_card.all().count() != 0:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('Please Add Payment'))
            return redirect('accounts:add_credit_card')


class UserHassApprovedConnection:
    def dispatch(self, request, *args, **kwargs):
        if request.user.user_connection.status == '1':
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(
                request, ('Please Wait Untiill Your Connection Is Accepted'))
            return redirect('gas:view_connection', request.user.user_connection.id)
