from django.urls import path
from . import views
app_name = "gas"

urlpatterns = [
    path('new-connection/', views.NewConnectionView.as_view(), name="new_connection"),
    path('view-connection/<int:pk>/', views.DetailConnectionView.as_view(),
         name="view_connection"),
    path('update-connection/<int:pk>/', views.UpdateConnectionView.as_view(),
         name="update_connection"),

    path('user/approved-connection/<int:pk>/', views.ApprovedConnectionView.as_view(),
         name="approved_connection"),

    path('book/cylinder/<int:connection_id>/',
         views.BookingCylinderView.as_view(), name='booking_cylinder'),

    path('booking/list/', views.BookingListView.as_view(), name='booking_list'),

    path('booking/detail/<int:pk>/',
         views.BookingDetailView.as_view(), name='booking_detail')
]
