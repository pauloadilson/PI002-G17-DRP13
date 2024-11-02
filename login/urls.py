from django.urls import path, include
from .views import CallbackView, CustomLoginView, SignInView, SignOutView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='signout'), name='logout'),
    path('microsoft_signin', SignInView.as_view(), name='signin'),
    path('microsoft_signout', SignOutView.as_view(), name='signout'),
    path('callback/', CallbackView.as_view(), name='callback'),
    
]