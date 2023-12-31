from django.urls import path, include
from website import views

urlpatterns = [
    path('', views.index, name='index view'),
    path('home/', views.home_view, name='home view'),
    path('create-payment/', views.CreatePayment.as_view(), name='create payment view'),
    path('accounts/', include([
            path('register/', views.UserRegistrationView.as_view(), name='user register'),
            # path('login/', views.UserLoginView.as_view(), name='login view'),
            path('details/', views.account_details, name='account details')
        ])
    ),
    path('logout/', views.logout_view, name='logout user'),
    path('custom-chart/', views.custom_chart, name='custom chart'), 
    path('contacts/', views.contacts, name='contacts'),
    path('payment/<int:pk>/delete/', views.DeletePaymentView.as_view(), name='delete payment'),
    path('payment/<int:pk>/edit/', views.EditPaymentView.as_view(), name='edit payment'),
]