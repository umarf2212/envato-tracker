from django.contrib import admin
from django.urls import path, include
from scraper import views as scraper_views

urlpatterns = [
    path('', scraper_views.home),
    path('show/', scraper_views.ShowRecords),
    path('admin/', admin.site.urls),
    path('scraper/', include('scraper.urls')),
    path('ATriggerVerify.txt', scraper_views.ATriggerVerify),
]