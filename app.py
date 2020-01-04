#  import dependancies

from flask import Flask, jsonify, render_template
from flask_cors import CORS, cross_origin
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime;


# Database Setup

engine = create_engine("sqlite:///NPSBioDiversity.db")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save reference to the table
National_parks = Base.classes.national_parks
Species = Base.classes.species

#  Flask Setup
#################################################
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/keepalive")
def keep_alive():
    return datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

# Get Species by Park Code
@app.route("/api/park/<park_code>/species")
@cross_origin()
def species_by_park(park_code):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Species.speciesID, Species.scientific_name, Species.family, Species.species_order,Species.category).filter(Species.park_code == park_code).all()
    
    session.close()
    spieces_totals = []
    for result in results:
        row = {}
        row['speciesID'] = result[0]
        row["scientificName"] = result[1]
        row["family"] = result[2]
        row['speciesOrder'] = result[3]
        row["category"] = result[4]
        spieces_totals.append(row)

    return jsonify(spieces_totals)

@app.route("/api/park")
@cross_origin()
def park_info():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(National_parks.park_code, National_parks.park_name, National_parks.state, National_parks.acres,National_parks.visitors, National_parks.latitude,National_parks.longitude).all()
    session.close()
    total_park = []
    for result in results[1:]:
        row = {}
        row['park_code'] = result[0]
        row["park_name"] = result[1]
        row["state"] = result[2]
        row['acres'] = result[3]
        row["visitors"] = result[4]
        row["latitude"] = result[5]
        row["longitude"] = result[6]
        total_park.append(row)

    return jsonify(total_park)


if __name__ == '__main__':
    app.run(debug=True)

