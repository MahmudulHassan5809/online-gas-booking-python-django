from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import datetime
from django.utils.timezone import now, localtime
from accounts.mixins import AictiveUserRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from gas.models import Connection
from gas.forms import ConnectionForm
from django.views import View, generic
# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'landing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class NewConnectionView(SuccessMessageMixin, AictiveUserRequiredMixin, generic.edit.CreateView):
    model = Connection
    template_name = 'connection/new_connection.html'
    form_class = ConnectionForm
    success_message = 'New Connection Created Successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Connection'
        return context

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NewConnectionView, self).form_valid(form)


class DetailConnectionView(SuccessMessageMixin, AictiveUserRequiredMixin, generic.detail.DetailView):
    model = Connection
    context_object_name = 'connection'
    template_name = 'connection/view_connection.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status='1')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class UpdateConnectionView(SuccessMessageMixin, AictiveUserRequiredMixin, generic.edit.UpdateView):
    model = Connection
    context_object_name = 'connection'
    template_name = 'connection/update_connection.html'
    form_class = ConnectionForm
    success_message = 'Connection Updated Successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Connection'
        return context

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        form_kwargs["update"] = True
        return form_kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdateConnectionView, self).form_valid(form)


class ApprovedConnectionView(AictiveUserRequiredMixin, generic.ListView):
    model = Connection
    context_object_name = 'connection_list'
    template_name = 'connection/approved_connection.html'

    def get_queryset(self):
        qs = Connection.objects.select_related('user').filter(status='1').only(
            'connection_number', 'name', 'email', 'mobile', 'address', 'user__username')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Approved Connection'
        return context
