from django.db import connection
from bs4 import BeautifulSoup
import requests
import json
import time

from scraper.models import ProductData

"""
Parameters
number_of_pages : number of pages to scrape data from
url : takes url of any envato store

Returns: JSON dictionary of all the product data.
"""
def scrape_data(url):
		
	#--Send GET to the URL and get the response
	url = requests.get(url)

	#--Fetch response as HTML
	c = url.content

	#--Parse the response HTML
	soup = BeautifulSoup(c, "html.parser")

	#--Find the <script> tag in which JSON data is present
	script = soup.find_all('script')
	script = script[1].string

	#--Clean up the JSON data
	script = script.replace('window.INITIAL_STATE=', '')
	script = script.replace('; window.dataLayer=[]', '')
	
	#--Parse JSON, ignore non UTF-8 chars
	data = json.loads(script, strict=False)
	data = data['searchPage']['results']['matches']

	#--Return dictionary
	return data

"""
Insert product details from dictionary into the 
Model.
"""
def ProductDataIntoModel(d_dict):
	for i in range(30):
		product_details = d_dict[i]

		AddProduct = ProductData(
			product_id = product_details['id'],
			sales = product_details['number_of_sales'],
			rating = str(product_details['rating']),
			price_cents = product_details['price_cents'],
			trending = product_details['trending'],
			scrape_time = time.time(),
			updated_at = product_details['updated_at'],
			site = product_details['site']
		)
		AddProduct.save()
	return True

"""
(Deprecated)
Inserts all the product related data into the database,
using raw SQL queries.
30 items per page.

Usage:--

	fetch_url = 'https://themeforest.net/search/wordpress?sort=sales'
	for page in range(1, 2):
		url = fetch_url + '&page={}'.format(page)
		items_dict = scrape_data(url)
		insert_data(items_dict)

"""
def insert_data(d_dict):
	with connection.cursor() as cursor:
		for i in range(30):
			product_details = d_dict[i]

			item_id 		= product_details['id']
			name 			= product_details['name']
			classn 			= product_details['classification']
			price_cents 	= product_details['price_cents']
			sales 			= product_details['number_of_sales']
			author 			= product_details['author_username']
			author_url 		= product_details['author_url']
			url 			= product_details['url']
			site 			= product_details['site']
			rating 			= str(product_details['rating'])
			updated_at 		= product_details['updated_at']
			trending 		= product_details['trending']
			tags 			= str(product_details['tags'])
			scrape_time 	= time.time()

			query = '''INSERT INTO envato_products \
			(item_id, name, classification, price_cents, sales, author, author_url, \
			url, rating, updated_at, trending, tags, scrape_time, site) \
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

			cursor.execute(query, (item_id, name, classn, price_cents, sales, author, author_url, url, \
			rating, updated_at, trending, tags, scrape_time, site))
	
	return True


"""
(Deprecated)
Inserts the number of sales and other stats into the database,
using raw SQL queries.
Usage:--

	fetch_url = 'https://themeforest.net/search/wordpress?sort=sales'
	items_dict = scrape_data(fetch_url)
	insert_sales_data(items_dict)

"""
def insert_sales_data(d_dict):
	with connection.cursor() as cursor:
		for i in range(30):
			product_details = d_dict[i]
			item_id 		= product_details['id']
			sales 			= product_details['number_of_sales']
			rating 			= str(product_details['rating'])
			updated_at 		= product_details['updated_at']
			price_cents 	= product_details['price_cents']
			trending 		= product_details['trending']
			site 			= product_details['site']
			scrape_time 	= time.time()

			query = '''INSERT INTO product_sales (product_id, sales, rating, price_cents, trending, \
			scrape_time, updated_at, site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''

			cursor.execute(query, (item_id, sales, rating, price_cents, trending, scrape_time, updated_at, site))

	return True
