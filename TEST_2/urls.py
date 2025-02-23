"""
URL configuration for TEST_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from transaction.views import TransactionListView, TransactionCreateView, export_transactions_excel


urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction_list'),
    path('add/', TransactionCreateView.as_view(), name='transaction_create'),
    path('export/', export_transactions_excel, name='export_transactions_excel'),

]