"""
URL configuration for iia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('favicon.ico/', views.home_logo, name='home_logo'),
    path(r'res/<str:file>/',views.home_res, name='home_res'),
    path('<str:app_name>/', views.app_home, name='app_home'),
    re_path(r'^(?P<app_name>\w+)/(?P<app_function>\w+)/$', views.app_function, name='app_function')
]
