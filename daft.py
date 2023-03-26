from bs4 import BeautifulSoup
from csv import writer
import requests, re, datetime

# find the page, run every day 6pm
# add a page for all Properties in Ireland
# If the total number passes 4500, the price is likely to go down
# 16,463 in ireland on 7 Mar, 16512 on 13-20 Mar
dublin_url = "https://www.daft.ie/property-for-sale/dublin"
south_house_url = "https://www.daft.ie/property-for-sale/south-co-dublin-dublin?salePrice_to=550000&floorSize_from=95&numBeds_from=3&propertyType=detached-houses&propertyType=semi-detached-houses"
d16_url = "https://www.daft.ie/property-for-sale/dublin-16-dublin?salePrice_to=550000&floorSize_from=95&numBeds_from=3&propertyType=detached-houses&propertyType=semi-detached-houses&pageSize=20"
d16_url2 = "https://www.daft.ie/property-for-sale/dublin-16-dublin?salePrice_to=550000&floorSize_from=95&numBeds_from=3&propertyType=detached-houses&propertyType=semi-detached-houses&pageSize=20&from=20"

date = str(datetime.date.today())

# request the pages
number_class = 'styles__SearchH1-sc-1t5gb6v-3 guZHZl'
price_class = 'TitleBlock__StyledCustomHeading-sc-1avkvav-5 blbeVq'

def get_web_content(url, html_level, html_class):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    if html_level == 'h3':
        property_info = soup.find_all(html_level, class_ = html_class)
    else:
        property_info = soup.find(html_level, class_ = html_class)
    return property_info

# get the data from each url
total_number = get_web_content(dublin_url, 'h1', number_class).text
total_num = ''.join(re.findall(r'\d+', total_number))

house_number = get_web_content(south_house_url, 'h1', number_class).text
house_num = re.findall(r'\d+', house_number)[0]

d16_number = get_web_content(d16_url, 'h1', number_class).text
d16_num = re.findall(r'\d+', d16_number)[0]

d16_prices = get_web_content(d16_url, 'h3', price_class)
d16_prices2 = get_web_content(d16_url2, 'h3', price_class)

d16_prices += d16_prices2

# calculate the average price of D16
d16_total_prices = []
chars = ['€', ',']

for price in d16_prices:
    price = price.text
    for char in chars:
        price = price.replace(char, '')
    d16_total_prices.append(int(price))

average_price = sum(d16_total_prices)/len(d16_total_prices)
d16_average_price = round(average_price)

# write the daily property data into the csv file 
file = open('housing.csv', 'a', encoding='utf8', newline='')
# logging: should add a funtion to report bug if the file doesn't exist
thewriter = writer(file)

info = [date, total_num, house_num, d16_num, d16_average_price]
thewriter.writerow(info)

print(info)