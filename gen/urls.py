from django.urls import path
from.import views

urlpatterns = [
    path('', views.index),
    path('generateCertificates/', views.generate),
    path('generateExcelSheet/', views.generate_sheet),
]