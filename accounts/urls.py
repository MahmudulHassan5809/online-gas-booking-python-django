from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

app_name = "accounts"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard_view'),
    path('my-profile/', views.MyProfileView.as_view(), name="my_profile"),

    path('add-credit-card/', views.AddCreditCardView.as_view(),
         name="add_credit_card"),
    path('payment-details/', views.PaymentDetailsView.as_view(),
         name="payment_details"),
    path('edit-credit-card/<int:pk>/', views.EditCreditCardView.as_view(),
         name="edit_credit_card"),
    path('delete-credit-card/<int:pk>/', views.DeleteCreditCardView.as_view(),
         name="delete_credit_card"),

    path('change-password/', views.ChangePasswordView.as_view(),
         name="change_password"),
    path('logout/', auth_views.LogoutView.as_view(template_name='landing/logout.html',
                                                  extra_context={'title': 'Logout', }), name="logout"),

    path('user/dashboard/',
         views.UserDashboardView.as_view(), name="user_dashboard"),



    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy(
        'accounts:password_reset_complete')),
        name="password_reset_confirm"),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
