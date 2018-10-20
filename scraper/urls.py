from django.urls import include, path
from django.conf.urls import url
from scraper import views

urlpatterns = [
	path('', views.home),
	url(r'^themeforest/wordpress/(\d+)/$', views.themeforest_wordress_top_seller),
	url(r'^themeforest/site-templates/(\d+)/$', views.themeforest_html_site_templates_top_seller),
	url(r'^codecanyon/wordpress/(\d+)/$', views.codecanyon_wordpress_top_seller),
	url(r'^codecanyon/php-scripts/(\d+)/$', views.codecanyon_php_scripts_top_seller),
	url(r'^codecanyon/javascript/(\d+)/$', views.codecanyon_javascript_top_seller),
	url(r'^ATriggerVerify.txt', views.ATriggerVerify),
	url(r'^one/(\d+)/$', views.one),
	#(?P<arg>[\w\-]+)
]