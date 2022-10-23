from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import *
from .models import *


class HomeIndexView(ListView):
    template_name = 'home/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('-id')[:5]


class UserLoginView(LoginView):
    model = User
    template_name = "users/login.html"
    success_url = '/'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin'
        return self.success_url


class UserLogoutView(LoginRequiredMixin, LogoutView):
    login_required()


class UserRegisterView(CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'users/register.html'
    success_url = '/login'


class ProductShowView(DetailView):
    model = Product
    template_name = 'products/show.html'


class ProductIndexView(ListView):
    template_name = 'products/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.order_by('-id')


@login_required
def order(request, product_id):
    Order(
        user_id=request.user.id,
        product_id=product_id
    ).save()
    return redirect('/profile')


class UserProfileView(ListView, LoginRequiredMixin):
    login_required()
    template_name = 'users/profile.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)[::-1]


class ProductSearchView(ListView):
    template_name = 'products/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(title__contains=self.request.GET.get('search'))
