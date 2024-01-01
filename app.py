from flask import Flask, jsonify
import pandas as pd
import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
import sqlite3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import json

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
#session = Session(engine)
Measurements = Base.classes.measurement
Station = Base.classes.station


#flask setup
app = Flask(__name__)
#flask routes
@app.route("/")
def homepage():
    return(
     """List all available api routes."""
        f"Available routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>"        
    )
@app.route('/api/v1.0/precipitation')
def get_column_values():
    session = Session(engine)
    response = session.query(Measurements.date, Measurements.prcp).all()
    response_df = pd.DataFrame(response)
    session.close()
    return response_df.to_json(orient = "records")
@app.route('/api/v1.0/stations')
def get_station_values():
    session = Session(engine)
    station_name_response = session.query(Station.station).all()
    station_name_response_df = pd.DataFrame(station_name_response)
    session.close()
    return station_name_response_df.station.tolist() 
   
@app.route('/api/v1.0/tobs')
def get_temperature_values():
    session = Session(engine)
    highest_date = session.query(func.max(Measurements.date)).scalar()
    s = highest_date.split("-")
    a=[]
    a.append(int(s[0]))
    a.append(int(s[1]))
    a.append(int(s[2]))
    most_recent_year = dt.date(2017,8,23)-dt.timedelta(days = 365)
   # response = session.query(Measurements.tobs).filter(Measurements.date > most_recent_year).all()
    response_chosen_station = session.query(Measurements.station, Measurements.tobs, Measurements.date).filter(Measurements.date >most_recent_year).all()
       
    session.close() # find the maximum activity in station according to the num of dates recorded
    tobs_df = pd.DataFrame(response_chosen_station)
    count_stationfreq=tobs_df.groupby('station')['date'].count()
    sorted_countstationfreq = count_stationfreq.sort_values(ascending =False)
    stationuniquecount=tobs_df['station'].nunique()
    stationuniquecount_df = stationuniquecount.to_json()
    list_tobs = tobs_df.to_json(orient = "records") #list of tobs for the most_recent_year for last year
    return stationuniquecount_df
@app.route('/api/v1.0/2017-08-1')
def get_s_date():
    session = Session(engine)
    start_date = dt.date(2017,8,1)
    tmin = session.query(func.min(Measurements.tobs)).filter(Measurements.date >= start_date).scalar()
    a = []
    a.append(tmin)
   
    #summary_array = [tmin, tmax, tmean]
    session.close()
    return a
                      
if __name__ == '__main__':
    app.run(debug=True)
    