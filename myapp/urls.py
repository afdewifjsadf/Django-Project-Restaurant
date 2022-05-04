from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
urlpatterns = [
    path('', views.index, name="index"),
    path('update_item/', views.updateItem, name="update_item"),
    path('cart/', views.cart, name="cart"),
    path('login/',views.loginPage, name="login"),
    path('register/',views.registerPage, name="register"),
    path('logout/',views.logoutUser, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('account/', views.accountPage, name="account"),
    path('report/', views.repostPage, name="report"),
    path('pdf_report', views.GeneratePdf.as_view(), name="pdfreport"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('updateOrder/<str:pk>/', views.updateOrder, name="updateOrder"),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name="deleteOrder"),

    path('password_reset/', 
    auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        success_url=reverse_lazy('myapp:password_reset_done')
    ), 
    name='password_reset'),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_sent.html'
        ), 
        name="password_reset_done"),

    path('password_reset_<uidb64>_<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_form.html",
            success_url=reverse_lazy('myapp:password_reset_complete')
     ), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_done.html"
        ), 
        name="password_reset_complete"),
]
