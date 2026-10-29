"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login),
    # path("login/", views.TestView.as_view()),
    path("index/", views.index),
    path("", views.login),
    # path("", views.TestView.as_view()),
    path("dashboard/",views.dashboard),
    path("top/",views.top),
    path("left/",views.left),
    path("elderlist/",views.elderlist),
    path("elderadd/",views.elderadd),
    path("elderdel/",views.elderdel),
    path("elderGetByid/",views.elderGetByid),
    path("elderupdate/",views.elderupdate),
    path("healthdata/",views.healthdata),
    path("camerainfo/",views.camerainfo),
    path("threshold/",views.threshold),
    path("healthdataadd/",views.healthdataadd),
    path("healthdatadel/",views.healthdatadel),
    path("healthdataupdate/",views.healthdataupdate),
    path("getelderbyname/",views.getelderbyname),
    path("getHealthDataByDate/",views.getHealthDataByDate),
    path("dailyreport/",views.daily_report_view),
    path("behaviorrecord/",views.behaviorrecord),
    path("dailyreportadd/",views.dailyreportadd),
    path("dailyreportupdate/",views.dailyreportupdate),
    path("dailyreportdel/",views.dailyreportdel),
    path("daily_report_view/",views.daily_report_view),
    path("book/",views.book),


]
