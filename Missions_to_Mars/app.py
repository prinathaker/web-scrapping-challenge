from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars
from pymongo import MongoClient

app = Flask(__name__)

#create connection variable
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

#mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
#mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
# Grab Value out of MongoDB
# Render Homepage Template
# Template needs to contain a button that links to the scrape route
# Needs to display the data pulled from MongoDB
@app.route("/")
def index():
    final_mars_data = mongo.db.final_mars_data.find_one()
    return render_template("index.html", mars_data=final_mars_data)

# final_mars_data  is the instance/name of mongo collection. its created in Mongo DB when scrape runs
# Create final_mars_data Entry in MongoDB
# Run the Scrape function from the scrape_mars.py file that we imported
# store the scraped data returned from the scrape() function
# Update Mongo DB final_mars_data collection with scraped data
# redirect back to the homepage
@app.route("/scrape")
def scrape():
    final_mars_data = mongo.db.final_mars_data
    marspages = scrape_mars.scrape()
    final_mars_data.update_one({},{"$set":marspages},upsert=True)
    #mars_data.update({},final_mars_data, upsert = True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)