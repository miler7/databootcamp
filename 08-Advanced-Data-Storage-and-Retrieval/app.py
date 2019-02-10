# Import Flask
from flask import Flask, jsonify, request

# Import numpy, pandas, and datetime
import numpy as np
import pandas as pd
from datetime import datetime

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Create an app 
app = Flask(__name__)

# Home page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return """
            <h1>Welcome to the Climate App Home Page!</h1>
            Here are the available routes:
            <br><a href="/api/v1.0/precipitation">Precipitation</a> 
            <br><a href="/api/v1.0/stations">Stations</a> 
            <br><a href="/api/v1.0/tobs">Temperature Observations</a> 
            <br><a href="/api/v1.0/<start>">Date Range</a> 
            """

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Pass in MySQL Connection
conn = engine.connect()

# Create measurement dataframe
mdata1 = pd.read_sql("SELECT * FROM Measurement", conn)

# Create station dataframe
sdata1 = pd.read_sql("SELECT * FROM Station", conn)

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    measurement_results = session.query(Measurement).all()
    precipitation_data = []
    for measurement in measurement_results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["prcp"] = measurement.prcp
        precipitation_data.append(measurement_dict)
    return jsonify(precipitation_data)

# Stations
@app.route("/api/v1.0/stations")
def station():
    station_results = session.query(Station).all()
    station_data = []
    for station in station_results:
        station_dict = {}
        station_dict["station"] = station.station
        station_data.append(station_dict)
    return jsonify(station_data)

# Temperature Observations
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement).\
        filter(Measurement.date >= '2016-08-23').all()
    tobs_data = []
    for tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = tobs.date
        tobs_dict["tobs"] = tobs.tobs
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

################ I couldn't get this last part to work, but wanted to try to get partial credit but not prevent my program from running the rest, so I commented it out.

# User range only start
# @app.route("/api/v1.0/<start>/<end>")
# def range():
#     range_results = session.query(Measurement).\
#         filter(Measurement.date >= 'start' & <= 'end').all()
#     range_data = []
#     range_dict[0] = min(d['tobs'] for d in range_results
#     range_dict[1] = max(d['tobs'] for d in range_results
#     range_dict[2] = float(sum(d['tobs'] for d in range_results)) / len(range_results)
#     range_data.append(range_dict)
#     jsonify(range_data)

if __name__ == "__main__":
    app.run(debug=True)
