from django.urls import path
from .views import *
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page

app_name = 'massmedia'

urlpatterns = [
    path('index/', TemplateView.as_view(template_name="massmedia/index.html"), name="index"),
    path('', login_redirect, name="login_redirect"),
    path('login_redirect/', login_redirect, name="login_redirect"),
    path('accounts/login/', cache_page(60*60*8)(auth_views.LoginView.as_view(template_name="massmedia/login.html")), name='login'),
    path('accounts/logout/', cache_page(60*60*8)(auth_views.LogoutView.as_view(next_page="/")), name='logout'),

    path('search/', SearchView.as_view(), name='search'),
]
