from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import datetime
from django.utils.timezone import now, localtime
from accounts.mixins import AictiveUserRequiredMixin, UserHasPaymentSystem, UserHassApprovedConnection
from django.contrib.messages.views import SuccessMessageMixin

from gas.models import Connection, Booking, GasReffiling
from gas.forms import ConnectionForm, BookingForm
from django.views import View, generic
# Create your views here.


class HomeView(generic.ListView):
    model = GasReffiling
    context_object_name = 'cylinder_list'
    paginate_by = 10
    template_name = 'landing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cylinder List'
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

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(status='1')

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


class BookingCylinderView(UserHasPaymentSystem, UserHassApprovedConnection, SuccessMessageMixin, AictiveUserRequiredMixin, generic.CreateView):
    model = Booking
    template_name = 'booking/booking_cylinder.html'
    form_class = BookingForm
    success_message = 'Cylinder Booked Successfully'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Booking Cylinder'
        context['connection_id'] = self.kwargs.get('connection_id')
        return context

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse_lazy('gas:booking_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.connection = get_object_or_404(
            Connection, id=self.kwargs.get('connection_id'))
        return super(BookingCylinderView, self).form_valid(form)


class BookingListView(AictiveUserRequiredMixin, generic.ListView):
    model = Booking
    context_object_name = 'booking_list'
    template_name = 'booking/booking_list.html'
    form_class = BookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Booking List'
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('type') == 'confirm':
            return qs.select_related('connection', 'reffiling').filter(user=self.request.user, status='1')
        elif self.request.GET.get('type') == 'on_the_way':

            return qs.select_related('connection', 'reffiling').filter(user=self.request.user, status='2')
        elif self.request.GET.get('type') == 'completed':

            return qs.select_related('connection', 'reffiling').filter(user=self.request.user, status='3')

        return qs.select_related('connection', 'reffiling').filter(user=self.request.user)


class BookingDetailView(AictiveUserRequiredMixin, generic.DetailView):
    model = Booking
    context_object_name = 'booking'
    template_name = 'booking/booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Booking Detail'
        return context
