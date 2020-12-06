# Import Flask
from flask import Flask, jsonify

# Dependencies and Setup
import numpy as np
import datetime as dt

# Python SQL Toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Pull dates
one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

# Flask Routes
# Home Route
@app.route("/")
def welcome():
        return """<html>
<h1>SQLAlchemy Homework - Surfs Up!</h1>
<p>Precipitation Analysis:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station Analysis:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature Analysis:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/yyyy-mm-dd">/api/v1.0/start</a></li>
</ul>
<p>Start & End Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/yyyy-mm-dd/yyyy-mm-dd">/api/v1.0/start/end</a></li>
</ul>
</html>
"""

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value
        session = Session(engine)
        prcp_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        session.close()
        # Convert List of Tuples into a Dictionary
        prcp_data_list = dict(prcp_data)
        # Return JSON Representation of Dictionary
        return jsonify(prcp_data_list)

# Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Return a JSON List of Stations From the Dataset
        session = Session(engine)
        stations_all = session.query(Station.station, Station.name).all()
        session.close()
        # Convert List of Tuples Into Normal List
        station_list = list(np.ravel(stations_all))
        # Return a JSON List of Stations from the Dataset
        return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        session = Session(engine)
        # most_active_stations
        most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).first()
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                filter(Measurement.station==most_active_stations.station).\
                order_by(Measurement.date).all()
        session.close()
        # Convert List of Tuples Into Normal List
        tobs_data_list = list(np.ravel(tobs_data))
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        session = Session(engine)
        start_day = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
        session.close()
        # Convert List of Tuples Into Normal List
        start_day_list = list(np.ravel(start_day))
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_day_list)
        # To pull specific date data change yyyy-mm-dd to wanted date

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        session = Session(engine)
        start_end_day = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
        session.close()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(np.ravel(start_end_day))
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)
        # To pull specific date data change yyyy-mm-dd to wanted date

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)