"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app1 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^addfavor/', views.addfavor),
    url(r'^getreply/', views.getreply),
    url(r'^submitreply/', views.submitreply),
    url(r'^login/', views.login),
    url(r'^submitchat/', views.submitchat),
    url(r'^getchat/', views.getchat),
    url(r'^getchat2/', views.getchat2),
    url(r'^username/', views.username),
    url(r'^logout/', views.logout),
    url(r'^dragon/', views.dragon),
]
