from django.urls import path, include
from .views import CustomLoginView, sign_in, sign_out, callback
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='signout'), name='logout'),
    path('microsoft_signin', sign_in, name='signin'),
    path('microsoft_signout', sign_out, name='signout'),
    path('microsoft_callback', callback, name='callback'),
]