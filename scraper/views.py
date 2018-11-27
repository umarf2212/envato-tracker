from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from scraper.models import ProductData
from scraper.BS4 import scrape_data, ProductDataIntoModel

def home(request):
	return HttpResponse('Index')

def ShowRecords(request):
	product_list = ProductData.objects.all()
	page = request.GET.get('page', 1)

	paginator = Paginator(product_list, 10)

	try:
		records = paginator.page(page)
	except PageNotAnInteger:
		records = paginator.page(1)
	except EmptyPage:
		records = paginator.page(paginator.num_pages)
	
	x = records.number - 3 if records.number > 4 else 1
	y = paginator.num_pages if records.number + 4 > paginator.num_pages else records.number + 4
	page_range = range(x, y)

	return render(request, 'home.html', {
		'records': records,
		'page_range': page_range
	})

# (Deprecated) Old school raw SQL
def showRecords(request):
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM product_sales')
		records = cursor.fetchall()
	
	return render(request, 'home.html', {
		'records': records
	})

def themeforest_wordress_top_seller(request, pages):
	for page in range(1, int(pages)+1):
		url = 'https://themeforest.net/category/wordpress?sort=sales&page={}'.format(page)
		data_dict = scrape_data(url)
		res = ProductDataIntoModel(data_dict)
	return HttpResponse('Ok.')

def themeforest_html_site_templates_top_seller(request, pages):
	for page in range(1, int(pages)+1):
		url = 'https://themeforest.net/category/site-templates?sort=sales&page={}'.format(str(page))
		data_dict = scrape_data(url)
		res = ProductDataIntoModel(data_dict)
	return HttpResponse('Ok.')

def codecanyon_wordpress_top_seller(request, pages):
	for page in range(1, int(pages)+1):
		url = 'https://codecanyon.net/category/wordpress?sort=sales&page={}'.format(str(page))
		data_dict = scrape_data(url)
		res = ProductDataIntoModel(data_dict)
	return HttpResponse('Ok.')

def codecanyon_php_scripts_top_seller(request, pages):
	for page in range(1, int(pages)+1):
		url = 'https://codecanyon.net/category/php-scripts?sort=sales&page={}'.format(str(page))
		data_dict = scrape_data(url)
		res = ProductDataIntoModel(data_dict)
	return HttpResponse('Ok.')

def codecanyon_javascript_top_seller(request, pages):
	for page in range(1, int(pages)+1):
		url = 'https://codecanyon.net/category/javascript?sort=sales&page={}'.format(str(page))
		data_dict = scrape_data(url)
		res = ProductDataIntoModel(data_dict)
	return HttpResponse('Ok.')

def ATriggerVerify(request):
	s = '''15C9E353DF430803972B3DB438921BE3

This is ATrigger.com API Verification File.
This file should be placed on the root folder of target url. This file is unique for each account in ATrigger.com
http://example.com/mySite/Task?name=joe        This file should be available at: http://example.com/ATriggerVerify.txt
http://sub.example.com/mySite/Task?name=joe    This file should be available at: http://sub.example.com/ATriggerVerify.txt

	'''
	return HttpResponse(s)

def one(request, pages):
	return HttpResponse(pages)
