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

    # Create master dictionary
    master = {'news_title': "NASA's Opportunity Rover Mission on Mars Comes to End",
        'news_p': "NASA's Opportunity Mars rover mission is complete after 15 years on Mars. Opportunity's record-breaking exploration laid the groundwork for future missions to the Red Planet.",
        'featured_image_url': 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA17470_hires.jpg',
        'mars_weather': 'Curiosity is again operating normally following a boot problem first experienced last Friday. Look for more Gale Crater weather conditions soon.\nhttps://www.jpl.nasa.gov/news/news.php?feature=7339\xa0…pic.twitter.com/gFMfXyeWDa',
        'hemisphere_image_urls': [{'title': 'Cerberus Hemisphere Enhanced',
        'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
        {'title': 'Schiaparelli Hemisphere Enhanced',
        'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
        {'title': 'Syrtis Major Hemisphere Enhanced',
        'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
        {'title': 'Valles Marineris Hemisphere Enhanced',
        'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]}

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

