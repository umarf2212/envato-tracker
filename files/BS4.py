import requests
import sqlite3
import json
import time
from bs4 import BeautifulSoup

####  OPEN DATABASE CONNECTION  ####
con = sqlite3.connect('../db.sqlite3')

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
Inserts all the product related data into the database.
30 items per page.

Usage:--

	fetch_url = 'https://themeforest.net/search/wordpress?sort=sales'
	for page in range(1, 2):
		url = fetch_url + '&page={}'.format(page)
		items_dict = scrape_data(url)
		insert_data(items_dict)

"""
def insert_data(d_dict):
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
	VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

		con.execute(query, (item_id, name, classn, price_cents, sales, author, author_url, url, \
	rating, updated_at, trending, tags, scrape_time, site))

		con.commit()


"""
Inserts the number of sales and other stats into the database.
Usage:--

	fetch_url = 'https://themeforest.net/search/wordpress?sort=sales'
	items_dict = scrape_data(fetch_url)
	insert_sales_data(items_dict)

"""
def insert_sales_data(d_dict):
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
		scrape_time, updated_at, site) VALUES (?,?,?,?,?,?,?,?)'''
		con.execute(query, (item_id, sales, rating, price_cents, trending, scrape_time, updated_at, site))
		con.commit()


"""
Checks if a record related to a given item_id exists.
Returns: True | False

Usage:--
	x = checkID(3840053)
	x = True/

"""
def checkID(item_id):
	q = "SELECT COUNT(item_id) FROM envato_products WHERE item_id = ? LIMIT 1"
	cur = con.execute(q, (item_id,))
	for r in cur:
		if r[0] > 0:
			return True
		else:
			return False

def printItemsData():
	q = "SELECT * FROM envato_products"
	cur = con.execute(q)

	for row in cur:
		s = ''
		for i in range(1,15):
			s += str(row[i]) + '\n' if i!=13 else str(row[i])
		print(s)

####  CLOSE DATABASE CONNECTION  ####
con.close()

#### DATABASE SCHEMA ####
"""
def products():
	conn = sqlite3.connect('../db.sqlite3')
	if conn is not None:
		conn.execute('''CREATE TABLE envato_products (
				id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				item_id INT(8),
				name VARCHAR(240),
				classification VARCHAR(100),
				price_cents INT(8),
				sales INT(8),
				author VARCHAR(50),
				author_url TEXT,
				url TEXT,
				rating VARCHAR(40),
				updated_at VARCHAR(30),
				trending BOOLEAN,
				tags TEXT,
				scrape_time VARCHAR(20));''')
		print('Table created successfully')
		conn.close()

##############################################################

def salesTable():
	conn = sqlite3.connect('../db.sqlite3')
	try:
		conn.execute('''CREATE TABLE product_sales (
				id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
				product_id INT(10) NOT NULL,
				sales INT(7) NOT NULL);''')
	except sqlite3.Error as err:
		print("Error:", err.message)

	conn.close()
"""

"""
DJANGO NOTES

To use database connection cursor and execute SQL queries inside django,
we can use django.db.connection module.

from django.db import connection

with connection.cursor() as cursor:
	cursor.execute('SOME SQL QUERY %s', [vars list])

This closes the connection automatically.

"""