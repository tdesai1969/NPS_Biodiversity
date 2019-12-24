#  import dependancies

from flask import Flask, jsonify
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

@app.route("/")
def welcome():
    return "Hello World, From Team TAMA!"

@app.route("/keepalive")
def keep_alive():
    return datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

# Get Species by Park Code
@app.route("/api/park/<park_code>/species")
def species_by_park(park_code):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Species.speciesID, Species.category,Species.species_order, Species.common_names).filter(Species.park_code == park_code).all()
    session.close()
    spieces_totals = []
    for result in results:
        row = {}
        row['speciesID'] = result[0]
        row["category"] = result[1]
        row['speciesOrder'] = result[2]
        row["commonNames"] = result[3]
        spieces_totals.append(row)

    return jsonify(spieces_totals)

if __name__ == '__main__':
    app.run(debug=True)

