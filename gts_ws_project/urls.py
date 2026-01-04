"""
URL configuration for gts_ws_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from core import views
from core.views_slack import slack_events

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('api/executive-summary/', views.executive_summary_api, name='executive_summary_api'),
    path('api/kpi-data/', views.kpi_data_api, name='kpi_data_api'),
    path('api/tariff-chart/', views.tariff_chart_data, name='tariff_chart_data'),
    path('api/tariffs/', views.tariffs_api, name='tariffs_api'),
    path('api/shipping/', views.shipping_api, name='shipping_api'),
    path('api/markets/', views.markets_api, name='markets_api'),
    path('api/dashboard/', views.dashboard_api, name='dashboard_api'),
    path('slack/events/', slack_events, name='slack_events'),
]
