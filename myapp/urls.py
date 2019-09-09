from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from .views import Disc, Dis

urlpatterns=[
    path('signup',views.signup,name='signup'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('accounts/login', views.loginView, name = 'accounts'),
    path('setpassword/<int:uid>',views.setpassword,name='setpassword'),
    path('accounts/password', views.change_password, name='change_password'),
    path('',login_required(Disc.as_view()), name='profile'),
    path('edit',views.edit_names, name='edit'),
    path('update', views.update_profile, name='update'),
    path('profileview',login_required(Dis.as_view()), name='profileview'),

]
