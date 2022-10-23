from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *


urlpatterns = [
    path('', HomeIndexView.as_view(), name="home.index"),
    path('login', UserLoginView.as_view(), name="users.login"),
    path('logout', UserLogoutView.as_view(), name="users.logout"),
    path('register', UserRegisterView.as_view(), name="users.register"),
    path('service', ProductIndexView.as_view(), name="products.index"),
    path('service/<int:pk>', ProductShowView.as_view(), name="products.show"),
    path('service/<product_id>/order', order, name="products.order"),
    path('profile', UserProfileView.as_view(), name="users.profile"),
    path('search_result', ProductSearchView.as_view(), name="products.search"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
