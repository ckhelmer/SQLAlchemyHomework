#Import libraries
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
import numpy as np
import datetime as dt

#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")

#Reflect the existing database
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station                       

#Create a session to query                       
session = Session(engine)                       

#Flask setup
app = Flask(__name__)

#Index page
@app.route("/")
def home():
   #List all the routes available 
   return("Welcome to the Hawaii Weather API </br>"
          f"Available Routes:</br>"
          f"</br>"
          f"To retrieve precipitation information: </br>"
          f"/api/v1.0/precipitation</br>"
          f"</br>"
          f"To retrieve a list of stations: </br>"
          f"/api/v1.0/stations</br>"
          f"</br>"
          f"To retrieve temperature information: </br>"
          f"/api/v1.0/tobs</br>"
          f"</br>"
          f"To retrieve a minimum, average, and maximum temperature for a specified date (Date  must have format YYYY-MM-DD)</br>"
          f"/api/v1.0/<start></br> "
          f"</br>"
          f"To retrieve a minimum, average, and maximum temperature between a specified date range (date range must have format YYYY-MM-DD): </br>"
          f"/api/v1.0/<start>/<end></br>")

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Retrieving precipitation")
    precip = session.query(Measurement.date, Measurement.prcp).all()
    precip2 = list(np.ravel(precip))                   
    return jsonify(precip2)
                       
@app.route("/api/v1.0/stations")
def stations():
    print("Retrieving stations")
    station_id = session.query((Measurement.station)).distinct().all()
    stations = list(np.ravel(station_id))
    return jsonify(stations)
    
@app.route("/api/v1.0/tobs")
def temperature():
    print("Retrieving temperatures")
    last_date = session.query(Measurement.date).\
    order_by(desc(Measurement.date)).first()
    
    ld = dt.datetime.strptime(last_date[0], "%Y-%m-%d")

    year = dt.timedelta(days = 365)
    last_year = ld - year
    last_year = last_year.date()
    
    temps = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > "2016-07-04").all()
    temps2 = list(np.ravel(temps))
    
    return jsonify(temps2)
    
@app.route("/api/v1.0/<start>")
def startdate(start):
    temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    temps2 = list(np.ravel(temps))
    
    return jsonify(temps2)
                          
@app.route("/api/v1.0/<start>/<end>")
def daterange(start, end):
    rangetemps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
              
    return jsonify(rangetemps)
    
if __name__ == "__main__":
    app.run(debug=True)
    