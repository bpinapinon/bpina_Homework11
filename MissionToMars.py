
# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
from splinter import Browser
import pandas as pd
# from selenium import webdriver ## for chromedriver if you just use {}'executable_path: 'chromedriver'} -- no .exe

####### MARS NEWS

# URL of page to be scraped
url_news = 'https://mars.nasa.gov/news/'


# splinter setup
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path)
browser.visit(url_news)

# Retrieve request module page
response = requests.get(url_news)
# Create BeautifulSoup object; parse 
soup = bs(response.text, 'lxml')

# Latest News Title from Mars News Site
titles = soup.find_all('div', class_='content_title')
news_title = titles[0].text
print(news_title)



# Latest News Paragraph Text from Mars News Site
paragraphs = soup.find_all('div', class_="rollover_description_inner")
news_p = paragraphs[0].text
print(news_p)

browser.quit()

##### MARS FEATURED IMAGE

# URL of JPL Mars Space Image 
# Scrape for featured image
url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

# Splinter setup
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)
browser.visit(url_images)

#sleep
time.sleep(5)

# Find and click the "full image" button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()

#sleep
time.sleep(5)

# Find the j"more info" button and click
more_info_elem = browser.find_link_by_partial_text('more info')
more_info_elem.click()


# Create object using BeautifulSoup and parse using 'html.parser'
html = browser.html
img_soup = bs(html, 'html.parser')


# find the relative image url 
img_url_rel = img_soup.find('figure', class_='lede').find('img')['src']
img_url_rel


# Use the base url to create absolute url (featured image)
JPL_link = 'https://www.jpl.nasa.gov'
featured_image_url = JPL_link + img_url_rel
featured_image_url


browser.quit()

###### MARS WEATHER


url_twitter = "https://twitter.com/marswxreport?lang=en"
response = requests.get(url_twitter)
soup = bs(response.text, 'html.parser')

result = soup.find('div', class_="js-tweet-text-container")
result

weather = result.p.text
weather


###### MARS FACTS

url_facts = "http://space-facts.com/mars/"

facts = pd.read_html(url_facts)[0]
facts.columns = ["description", "value"]
facts.set_index('description', inplace=True)
facts

# Convert panda dataframe to HTML table string
mars_facts_html = facts.to_html()
mars_facts_html



#### MARKS HEMISPHEERES


# Scraping USGS  
url_USGS = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# splinter setup
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path)
browser.visit(url_USGS)

html = browser.html
soup = bs(html, 'html.parser')

url_base = "https://astrogeology.usgs.gov"
result = soup.find_all('div', class_="item")

url_list = []

for y in result:
    link = y.find('a')['href']
    url_list.append(link)
    
print(url_list)


# Empty list to store dictionaries of image URL strings and  hemisphere title  
hemisphere_image_urls = []

for x in url_list:
    url = url_base + x
        
    browser.visit(url)
    
    # Sleep script to verify that the page loaded
    time.sleep(8)
    
    soup = bs(browser.html, 'html.parser')
    
    # Retrieve image url
    result_image = soup.find('img', class_="wide-image")
    image = url_base + result_image["src"]
    
    # Retrieve page title; remove "Enhanced" 
    result_title = soup.find('h2', class_='title')
    title = result_title.text
    title = title.rsplit(' ', 1)[0]
    
    diction = {"Title": title, "Image URL": image}
    hemisphere_image_urls.append(diction)
    
    time.sleep(10)
    
print(hemisphere_image_urls)

browser.quit()