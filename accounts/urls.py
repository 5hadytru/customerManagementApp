from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # name kwarg will act as an alias in template tags
    path('', views.home, name='home'),
    path('account/', views.accountSettings, name='account'),
    path('user/', views.userPage, name='user'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_order/<str:pk>', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),

    path('reset_password/', auth_views.PasswordResetView.as_view()),  # class based view
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view()),
    path('reset/<ubid64>/<token>/', auth_views.PasswordResetConfirmView.as_view()),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view()),

]
