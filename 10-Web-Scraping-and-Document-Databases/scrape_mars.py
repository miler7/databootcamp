# Import dependencies
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
import pymongo
import jinja2

 # Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.mars_db

# Create an app 
app = Flask(__name__)

# Create mongo function
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Create scrape route
@app.route("/scrape")

# Create function
def scrape():

    # # NASA Mars News

    # Create object
    result = requests.get("https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    # Scrape title
    news_title_chunk = soup.find('div', attrs={'class':'content_title'})
    news_title = news_title_chunk.find('a').text.strip()
    news_title

    # Scrape paragraph text
    news_p_chunk = soup.find('div', attrs={'class':'rollover_description_inner'})
    news_p = news_p_chunk.text.strip()
    news_p


    # # JPL Mars Space Images - Featured Image

    # Set up browser
    executable_path = {"executable_path": "/Users/theju/Anaconda3/pkgs/selenium-chromedriver-2.27-0/Library/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    # Go to url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Wait 10 seconds
    time.sleep(15)

    # Navigate to featured image full image
    image_link = browser.find_by_id('full_image')
    image_link.click()

    # Wait 10 seconds
    time.sleep(15)

    # Navigate to featured image details
    image_details = browser.find_link_by_partial_text('more info')
    image_details.click()

    # Wait 10 seconds
    time.sleep(15)

    # Determine featured image url
    featured_image_element = browser.find_link_by_partial_href("largesize")
    featured_image_url = featured_image_element["href"]
    featured_image_url


    # # Mars Weather

    # Create object
    result = requests.get("https://twitter.com/marswxreport?lang=en")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    # Scrape tweet
    mars_weather_chunk = soup.find('p', attrs={'class':'tweet-text'}).text
    mars_weather = mars_weather_chunk.replace("InSight ", "")
    mars_weather


    # # Mars Facts

    # Create object
    result = requests.get("https://space-facts.com/mars/")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    # Collect html table
    facts_html = soup.find('table', attrs={'class':'tablepress-id-mars'})
    facts_html


    # # Mars Hemispheres

    # Create object
    result = requests.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')

    # Collect titles in list
    title = []
    for div in soup.find_all("div", {"class":"item"}):
        for link in div.select("h3"):
            title.append(link.text)
    title

    # Set up browser
    executable_path = {"executable_path": "/Users/theju/Anaconda3/pkgs/selenium-chromedriver-2.27-0/Library/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    # Wait 10 seconds
    time.sleep(15)

    # Collect image urls in list
    img_url = []
    for div in soup.find_all("div", {"class":"item"}):
        for link in div.select("a.product-item"):
            url = 'https://astrogeology.usgs.gov' + link['href']
            browser.visit(url)
            full_image_element = browser.find_link_by_partial_href("download")
            full_image_url = full_image_element["href"]
            img_url.append(full_image_url)
    img_url

    # Combine lists into list of dictionaries
    hemisphere_image_urls = [{'title': title, 'img_url': img_url} for (title,img_url) in zip(title,img_url)]
    hemisphere_image_urls


    # Create master dictionary
    master = {}
    master["news_title"] = news_title
    master["news_p"] = news_p
    master["featured_image_url"] = featured_image_url
    master["mars_weather"] = mars_weather
    master["facts_html"] = facts_html
    master["hemisphere_image_urls"] = hemisphere_image_urls

    # Insert dictionary into MongoDB as a document
    collection.insert(master)

    # Return function
    return f"Done"

# Home page
@app.route("/")
def home_page():
    master = mongo.db.data.find()
    return render_template("index.html",
        master=master)

if __name__ == "__main__":
    app.run(debug=True)