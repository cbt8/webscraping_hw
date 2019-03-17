from flask import Flask, render_template, request, url_for, redirect
from mission_to_mars import news_p, news_title, featured_img_url, mars_weather, mars_facts, mars_hemispheres, scrape
from flask_bootstrap import Bootstrap
import pymongo


app = Flask(__name__)
Bootstrap(app)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.marsDB
#db.mars.delete_many({})
mars_collection = db.mars


#test = mars_collection.find({})
@app.route('/')
def index():
    
    test = mars_collection.find_one({})
    title = mars_collection.find_one({'title':"NASA's Opportunity Rover Mission on Mars Comes to End"})
    description = mars_collection.find_one({'description': "NASA's Opportunity Mars rover mission is complete after 15 years on Mars. Opportunity's record-breaking exploration laid the groundwork for future missions to the Red Planet."})
    #image = mars_collection.find_one({}['hemisphere'])




    return render_template('index.html',test=test, title=title, description=description)#, image=image)





if __name__ == "__main__":
    app.run(debug=True)