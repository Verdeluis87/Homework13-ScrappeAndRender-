from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # return Browser("chrome", **executable_path, headless=False)
    return Browser("chrome", headless=False)

def scrape():
    browser = init_browser()
    
    # scrape NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_p= soup.find('div', class_="article_teaser_body").text

    # JPL Mars Space Images - Featured Image
    # URL and sub-url to concatenate image_url to end of it
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    sub_url = 'https://www.jpl.nasa.gov'
    # visit site
    browser.visit(url_2)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    img_url = soup.find('div', class_='carousel_items').article['style']
    # strip image_url of unnecessary text
    strip_img_url = re.findall("\'(.*?)\'", img_url)
    # for some reason re.findall returns list, grab first element
    # to get final_img_url
    final_img_url = strip_img_url[0]
    # scraped image url
    featured_img_url = sub_url + final_img_url

    # Mars Weather
        # URL to get ethe latest tweet from the Mars Weather twitter account
    url = 'https://twitter.com/marswxreport?lang=en'

    # visit site
    browser.visit(url)
    time.sleep(1)
    html3 = browser.html
    soup = BeautifulSoup(html3, 'html.parser')

    tlist = soup.find_all("li", class_="js-stream-item")
    
    # Search through list for weather tweet

    for t in tlist:
        if t.div["data-screen-name"] == "MarsWxReport":
            mars_weather = t.find(class_="tweet-text").a.previousSibling
        break

    # Mars Facts
    url =('http://space-facts.com/mars')
    browser.visit(url)
    time.sleep(1)
    html3 = browser.html
    soup = BeautifulSoup(html3, 'html.parser')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    df.columns = [" ", " Value "]
    df = df.to_html(index = None, classes='width="100%" cellpadding=1 cellspacing=2 style="background-color: #ffffff;"')

    # Mars Hemispheres
    # URL to get ethe latest tweet from the Mars Weather twitter account
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # visit site
    browser.visit(url4)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Create an empty list to hold the URLS
    url_list = []
    categories = soup.find_all("div", class_="item")

    # Create a for loop to get all the URLS
    for category in categories:
        url = category.find('a')['href']
        url_list.append(url)

    url_img_list = ['https://astrogeology.usgs.gov' + url for url in url_list]

    img_url_list=[]

    for url in url_img_list:
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img = soup.find_all('a')[41]['href']
        img_url_list.append(img)
    


    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": f'{img_url_list[3]}'},
        {"title": "Cerberus Hemisphere", "img_url": f'{img_url_list[0]}'},
        {"title": "Schiaparelli Hemisphere", "img_url": f'{img_url_list[1]}'},
        {"title": "Syrtis Major Hemisphere", "img_url": f'{img_url_list[2]}'},
    ]

    listings = {
    "news_title" : news_title,
    "news_p" : news_p,
    "featured_image" : featured_img_url,
    "mars_weather" : mars_weather,
    "df" : df,
    "hemispheres" : hemisphere_image_urls,
    }

    return listings
