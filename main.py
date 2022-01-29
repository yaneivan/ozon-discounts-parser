from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import random

def remove_P(text):
	text = text.replace(' ₽', '')
	text = text.replace(' ', '')
	text = int(text)
	return text

def remove_discount_sign(text):
	text = text.replace('−', '')
	text = text.replace('%', '')
	return text

def make_a_list_of_page_links(category):
	mas = []
	for count in range(1, 4): #make 300 just for lol
		link = 'https://www.ozon.ru' + category + '?page='+str(count)
		mas.append(link)
	return mas

def parse_category_page(link):
	page = urlopen(link)
	html_text = page.read()
	#file = open('out.html', 'wb')
	#file.write(html_text)
	#file.close()
	soup = BeautifulSoup(html_text, 'lxml')

	items = soup.find_all(class_='h4k h5k')
	discount_class = 'f4c fc6 h0j'
	link_class = 'h6j tile-hover-target'

	if items == []:
		items = soup.find_all(class_ = 'h4k hk5')
	if items == []:
		items = soup.find_all(class_ = 'h6k k6h')
		discount_class = 'f4c cf5'
		link_class = 'tile-hover-target h8i'

	mas = []
	for i in items:
		price_of_the_item = i.find(class_ = 'ui-a4a ui-aa6', attrs={'style':'color:#001a34;'})
		if not(price_of_the_item):  #wow, we got a discount here

			new_price_of_item = i.find(class_='ui-a4a ui-aa6 ui-a7a').text
			old_price_of_item = i.find(class_ = 'ui-aa8 ui-aa6').text
			discount_of_item = i.find(class_ = discount_class, attrs={'style':'color:#fff;background-color:#f91155;'}).text
			
			old_price_of_item = remove_P(old_price_of_item)
			new_price_of_item = remove_P(new_price_of_item)
			discount_of_item = remove_discount_sign(discount_of_item)
			difference_between_prices = old_price_of_item - new_price_of_item

			link = 'ozon.ru' + i.find('a', class_ = link_class, href=True)['href']

			mas.append([difference_between_prices, new_price_of_item, old_price_of_item, discount_of_item, link])
	
	return mas
	
def go_through_every_category(categorys):
	somthin = []
	for category in categorys:
		global_result = []
		mas = make_a_list_of_page_links(category)
		for link in mas:
			print('Now getting:', link)
			time.sleep(random.randrange(5))
			result = parse_category_page(link)
			for i in result:
				global_result.append(i)
		global_result.sort(key = lambda x: x[0])
		for i in global_result:
			print(i)
		somthin.append(global_result)
	return somthin

def find_all_categorys():
	page = urlopen('https://www.ozon.ru')
	html_text = page.read()
	soup = BeautifulSoup(html_text, 'lxml')
	categorys = soup.find_all(class_ = 'fv9 p0b b1p')
	for i in range(len(categorys)):
		categorys[i] = categorys[i]['href']
	return categorys


print()
mas = find_all_categorys()	
mas1 = go_through_every_category(mas)
for i in range(len(mas)):
	print(mas[i])
	print(mas1[i][-1])
	print()