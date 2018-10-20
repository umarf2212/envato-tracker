from django.contrib import admin
from django.urls import path, include
from scraper import views

urlpatterns = [
    path('', views.home),
    path('show/', views.showRecords),
    path('admin/', admin.site.urls),
    path('scraper/', include('scraper.urls')),
    path('ATriggerVerify.txt', views.ATriggerVerify),
]